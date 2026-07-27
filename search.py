"""
BM25-based search engine for TeleBot Studio documentation.

Implements deterministic BM25 ranking with both unigram and bigram
tokenization, scoped search filters, heading-weighted boosting,
and thread-safe LRU caching for repeated queries.
"""

from __future__ import annotations

import heapq
import logging
import re
import threading
from collections import OrderedDict
from typing import ClassVar

from rank_bm25 import BM25Okapi

from loader import Chunk

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_.]+")


def tokenize(text: str) -> list[str]:
    """
    Convert text into searchable tokens (lowercase unigrams).

    Splits on non-alphanumeric characters except underscores and dots,
    which are preserved for technical identifiers like ``TeleBot.send_message``.
    """
    return _TOKEN_RE.findall(text.lower())


def tokenize_with_bigrams(text: str) -> list[str]:
    """
    Convert text into searchable tokens (lowercase unigrams AND bigrams).

    The README specifies: "Chunks are tokenized into lowercase unigrams
    and bigrams."  Bigrams help match multi-word API names like
    ``send_message`` or ``inline_keyboard``.

    This is the *corpus* tokenizer and is intentionally lossless — every
    document token stays in the index.  Query-side scaffolding removal is
    handled separately by :func:`tokenize_query`.
    """
    unigrams = tokenize(text)
    bigrams = [
        f"{unigrams[i]}_{unigrams[i + 1]}"
        for i in range(len(unigrams) - 1)
    ]
    return unigrams + bigrams


# Question scaffolding: the function words that make a natural-language query
# *sound* like a question without carrying any topic meaning.  Deliberately
# minimal — it contains only closed-class English function words and the
# generic verbs common to "How do I ..." phrasings.  It contains NO domain
# vocabulary, so no TeleBot Studio term can ever be filtered out.
#
# Why this exists: the corpus is indexed with unigrams *and* bigrams, so a
# query like "How do I use PIL in my TeleBot Studio bot?" contributes 18
# scaffolding tokens (``how``, ``do``, ``i``, ``how_do``, ``do_i`` ...) and
# exactly one topical token (``pil``).  Any chunk that merely *reads* like a
# question therefore outscores the chunk that actually answers it.  Dropping
# scaffolding from the QUERY only (never from the index) restores topical
# ranking while leaving stored documents untouched.
QUERY_STOPWORDS: frozenset[str] = frozenset({
    "a", "an", "the", "how", "do", "does", "did", "i", "me", "my", "we",
    "our", "you", "your", "is", "are", "was", "were", "be", "can", "could",
    "should", "would", "will", "what", "when", "where", "which", "who",
    "why", "to", "of", "for", "with", "and", "or", "in", "on", "at", "by",
    "from", "it", "its", "this", "that", "these", "those", "there", "here",
    "if", "then", "than", "so", "as", "up", "out", "about", "into",
    "use", "using", "used", "get", "make", "need",
})


def tokenize_query(text: str) -> list[str]:
    """
    Tokenize a *search query*, dropping question scaffolding.

    Identical to :func:`tokenize_with_bigrams` except that:

    - scaffolding unigrams (see :data:`QUERY_STOPWORDS`) are removed, and
    - bigrams made of two scaffolding words (``how_do``, ``do_i``) are
      dropped, while bigrams anchored by a real term (``send_message``,
      ``telegram_stars``) are kept.

    If a query consists *only* of scaffolding (e.g. ``"how do I"``), the
    unfiltered tokens are returned so the query still matches something
    rather than silently returning nothing.
    """
    unigrams = tokenize(text)

    bigrams = [
        f"{unigrams[i]}_{unigrams[i + 1]}"
        for i in range(len(unigrams) - 1)
        if not (
            unigrams[i] in QUERY_STOPWORDS
            and unigrams[i + 1] in QUERY_STOPWORDS
        )
    ]
    content = [w for w in unigrams if w not in QUERY_STOPWORDS]

    filtered = content + bigrams
    if not filtered:
        # Query was pure scaffolding — fall back to the unfiltered form.
        return unigrams + [
            f"{unigrams[i]}_{unigrams[i + 1]}"
            for i in range(len(unigrams) - 1)
        ]
    return filtered


# ---------------------------------------------------------------------------
# Thread-safe LRU Cache
# ---------------------------------------------------------------------------

class LRUCache:
    """Thread-safe LRU cache for search results.

    Caches (method, query, top_k) -> results so that repeated identical
    queries return instantly without re-scoring the entire corpus.
    """

    def __init__(self, maxsize: int = 256) -> None:
        self._cache: OrderedDict[str, list] = OrderedDict()
        self._maxsize = maxsize
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def _key(self, method: str, query: str, top_k: int) -> str:
        return f"{method}\x00{query}\x00{top_k}\x00v2"

    def get(self, method: str, query: str, top_k: int) -> list | None:
        k = self._key(method, query, top_k)
        with self._lock:
            if k in self._cache:
                self._cache.move_to_end(k)
                self._hits += 1
                return self._cache[k]
            self._misses += 1
            return None

    def put(self, method: str, query: str, top_k: int, results: list) -> None:
        k = self._key(method, query, top_k)
        with self._lock:
            if k in self._cache:
                self._cache.move_to_end(k)
            self._cache[k] = results
            if len(self._cache) > self._maxsize:
                self._cache.popitem(last=False)

    @property
    def maxsize(self) -> int:
        return self._maxsize

    @property
    def hits(self) -> int:
        with self._lock:
            return self._hits

    @property
    def misses(self) -> int:
        with self._lock:
            return self._misses


# ---------------------------------------------------------------------------
# Search Engine
# ---------------------------------------------------------------------------

class SearchEngine:
    """
    BM25-based search engine for markdown documentation chunks.

    Supports:
    - Full-text BM25 search across all chunks
    - Scoped searches (examples, API, library, functions, errors)
    - Heading-weighted score boosting
    - Page retrieval by filename
    - Page listing
    - Thread-safe LRU caching for repeated queries
    """

    # Keywords used to identify chunk categories for scoped search.
    # Words that are too short or too common are excluded to avoid
    # over-matching.  Phrases with spaces match more precisely.
    API_KEYWORDS: frozenset[str] = frozenset({
        "api", "endpoint", "parameter", "config", "configuration",
        "option", "setting", "argument", "return value", "response",
        "request", "method", "property", "attribute",
        "class", "object", "handler", "decorator",
    })

    LIBRARY_KEYWORDS: frozenset[str] = frozenset({
        "install", "installation", "import", "pip install", "dependency",
        "library", "package", "module", "requirement", "setup",
        "virtualenv", "venv", "requirements",
        "third-party", "extension", "plugin",
    })

    FUNCTION_KEYWORDS: frozenset[str] = frozenset({
        "def ", "function", "method", "class ", "async def",
        "lambda", "signature", "callback", "return ", "yield",
        "parameter", "argument", "telebot.", "bot.",
        "handler", "decorator",
    })

    ERROR_KEYWORDS: frozenset[str] = frozenset({
        "error", "exception", "traceback", "fault", "bug",
        "fail", "failed", "issue", "problem", "debug",
        "troubleshoot", "fix", "solve", "warning", "raise",
        "catch", "try", "except", "status code", "http error",
        "timeout", "refused", "denied", "not found", "invalid",
    })

    # Headings whose sections are *indexes of example user questions* rather
    # than documentation content.  In ``docs/patterns/`` every pattern page
    # ends with a "User Prompts This Pattern Solves" section that lists
    # question phrasings verbatim, e.g.:
    #
    #     - "How do I paginate a list in TeleBot Studio?"
    #     - "How do I add next and previous buttons to a list?"
    #
    # Because the corpus is tokenized into unigrams *and* bigrams with no
    # stopword filtering, these sections accumulate a dense concentration of
    # question scaffolding (``how``, ``do``, ``i``, ``how_do``, ``do_i``,
    # ``telebot_studio``).  Any question-shaped query therefore matches them
    # on a dozen or more tokens regardless of topic, so they outrank the
    # reference documentation that actually answers the question.
    #
    # These sections are still useful — they describe what a pattern solves —
    # so they remain fully indexed and retrievable.  They are simply damped
    # so that genuine documentation outranks them on generic questions, while
    # a query that really targets the pattern (which also matches the page's
    # topical terms) still surfaces it.
    PROMPT_INDEX_HEADINGS: frozenset[str] = frozenset({
        "user prompts this pattern solves",
    })

    # Damping multiplier applied to prompt-index sections.  Chosen empirically:
    # the smallest reduction that removes these chunks from the top of every
    # reproducing natural-language query, while keeping every pattern page
    # discoverable by its own pattern-intent query.  Stronger damping (<=0.35)
    # begins to hide legitimate pattern results.
    PROMPT_INDEX_WEIGHT: ClassVar[float] = 0.5

    # Heading level -> score multiplier (applied after BM25 scoring).
    # Higher structural importance (H1 page titles) gets a larger boost.
    # H4-H6 entries are provided for forward compatibility; the loader
    # currently keeps H4+ content inside the parent H1-H3 chunk, but
    # if that changes these weights will be ready.
    HEADING_WEIGHTS: ClassVar[dict[int, float]] = {
        0: 1.0,   # No heading (pre-heading content)
        1: 1.4,   # H1 — page titles, highest structural importance
        2: 1.2,   # H2 — major sections
        3: 1.1,   # H3 — subsections
        4: 1.05,  # H4 — sub-subsections, minimal boost
        5: 1.0,   # H5 — no boost (same as no heading)
        6: 1.0,   # H6 — no boost (same as no heading)
    }

    def __init__(self, chunks: list[Chunk], cache_size: int = 256) -> None:
        self.chunks = chunks
        self._cache = LRUCache(maxsize=cache_size)

        # Pre-compute combined text ONCE (fixes duplicate computation bug)
        self._chunk_texts: list[str] = [
            f"{chunk.title}\n{chunk.content}"
            for chunk in chunks
        ]

        # Build corpus with bigram-enhanced tokenization
        self.corpus = [
            tokenize_with_bigrams(text)
            for text in self._chunk_texts
        ]

        # Build chunk index for O(1) lookups (fixes O(n) index() scan)
        self._chunk_to_idx: dict[int, int] = {
            id(chunk): i for i, chunk in enumerate(chunks)
        }

        # Pre-compute the per-chunk score multiplier: heading weight, damped
        # for "prompt index" sections (see PROMPT_INDEX_HEADINGS).  Computed
        # once at construction so scoring stays a simple lookup.
        self._score_weights: list[float] = [
            self.HEADING_WEIGHTS.get(chunk.heading_level, 1.0)
            * (
                self.PROMPT_INDEX_WEIGHT
                if chunk.title.strip().lower() in self.PROMPT_INDEX_HEADINGS
                else 1.0
            )
            for chunk in chunks
        ]

        # Pre-compute category flags for each chunk (for scoped search)
        self._chunk_flags: list[dict[str, bool]] = []
        for i, text in enumerate(self._chunk_texts):
            text_lower = text.lower()
            self._chunk_flags.append({
                "has_code": "```" in chunks[i].content,
                "is_api": self._matches_keywords(text_lower, self.API_KEYWORDS),
                "is_library": self._matches_keywords(text_lower, self.LIBRARY_KEYWORDS),
                "is_function": self._matches_keywords(text_lower, self.FUNCTION_KEYWORDS),
                "is_error": self._matches_keywords(text_lower, self.ERROR_KEYWORDS),
            })

        # Pre-compute pages set (avoids rebuilding on every list_pages call)
        self._pages: list[str] = sorted({chunk.file for chunk in chunks})

        logger.info(
            "Building BM25 index with %d chunks (unigram + bigram tokenization)",
            len(chunks),
        )
        self.bm25 = BM25Okapi(self.corpus)
        logger.info("BM25 index ready")

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def chunk_flags(self) -> list[dict[str, bool]]:
        """Read-only access to category flags (for diagnostic tools)."""
        return self._chunk_flags

    @property
    def cache(self) -> LRUCache:
        """Read-only access to the LRU cache (for diagnostic tools)."""
        return self._cache

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        """
        Full-text BM25 search across all chunks.

        Returns a list of (chunk, score) tuples sorted by score descending.
        Only chunks with a positive BM25 score are included.

        Uses ``heapq.nlargest`` for O(n + k log n) performance instead
        of sorting all chunks at O(n log n).

        Heading weights are applied as multipliers to the BM25 scores
        before selecting top-k results.
        """
        # Check cache first
        cached = self._cache.get("search", query, top_k)
        if cached is not None:
            return cached

        tokens = tokenize_query(query)
        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)

        # Apply heading weights to BM25 scores
        weighted_scores = [
            float(scores[i]) * self._score_weights[i]
            for i in range(len(scores))
        ]

        # Use heapq.nlargest for efficient top-k extraction
        # Create (weighted_score, index) pairs and find the top-k
        scored_indices = [(weighted_scores[i], i) for i in range(len(weighted_scores))]
        top_scored = heapq.nlargest(top_k, scored_indices, key=lambda x: x[0])

        results: list[tuple[Chunk, float]] = []
        for score, idx in top_scored:
            if score <= 0:
                break  # All remaining are <= 0 since we used nlargest
            results.append((self.chunks[idx], score))

        # Cache the results
        self._cache.put("search", query, top_k, results)
        return results

    def get_page(self, filename: str) -> list[Chunk]:
        """
        Return all chunks belonging to a single markdown file.

        Matches by filename (case-insensitive), with or without the
        ``.md`` extension.  Returns chunks directly without scores
        since this is a direct retrieval, not a search.
        """
        filename = filename.lower().strip()
        filename_md = filename + ".md"
        return [
            chunk
            for chunk in self.chunks
            if chunk.file.lower() == filename
            or chunk.file.lower() == filename_md
        ]

    def list_pages(self) -> list[str]:
        """
        Return a sorted list of all unique markdown filenames.
        """
        return list(self._pages)  # Return a copy to prevent mutation

    def search_examples(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        """
        Scoped search that prefers chunks containing code blocks.

        Strategy:
        1. Run a broad search (top_k * 10 candidates).
        2. Filter to chunks containing code fences (using pre-computed flag).
        3. If code chunks exist, return them (up to top_k).
        4. Otherwise, fall back to the top generic results.
        """
        cached = self._cache.get("search_examples", query, top_k)
        if cached is not None:
            return cached

        broad_results = self.search(query, top_k=top_k * 10)

        # Use pre-computed has_code flag (consistent with other scoped searches)
        code_results = [
            (chunk, score) for chunk, score in broad_results
            if self._chunk_flags[self._chunk_to_idx[id(chunk)]]["has_code"]
        ]

        results = code_results[:top_k] if code_results else broad_results[:top_k]
        self._cache.put("search_examples", query, top_k, results)
        return results

    def search_api(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        """
        Scoped search restricted to API references, endpoints, and
        configuration parameters.
        """
        cached = self._cache.get("search_api", query, top_k)
        if cached is not None:
            return cached

        results = self._scoped_search(
            query, top_k, flag_key="is_api",
            title_keywords={"api", "function", "method", "library", "class"},
        )
        self._cache.put("search_api", query, top_k, results)
        return results

    def search_library(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        """
        Scoped search targeting library installations, imports, and
        third-party dependency information.
        """
        cached = self._cache.get("search_library", query, top_k)
        if cached is not None:
            return cached

        results = self._scoped_search(
            query, top_k, flag_key="is_library",
            title_keywords={"library", "install", "import", "module", "package"},
        )
        self._cache.put("search_library", query, top_k, results)
        return results

    def search_functions(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        """
        Scoped search targeting specific function definitions, signatures,
        and method explanations.
        """
        cached = self._cache.get("search_functions", query, top_k)
        if cached is not None:
            return cached

        results = self._scoped_search(
            query, top_k, flag_key="is_function",
            title_keywords={"function", "method", "def", "class", "callback"},
        )
        self._cache.put("search_functions", query, top_k, results)
        return results

    def search_errors(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        """
        Scoped search targeting error codes, exception handling,
        troubleshooting guides, and common pitfalls.
        """
        cached = self._cache.get("search_errors", query, top_k)
        if cached is not None:
            return cached

        results = self._scoped_search(
            query, top_k, flag_key="is_error",
            title_keywords={"error", "exception", "troubleshoot", "debug", "fix"},
        )
        self._cache.put("search_errors", query, top_k, results)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _scoped_search(
        self,
        query: str,
        top_k: int,
        flag_key: str,
        title_keywords: set[str],
    ) -> list[tuple[Chunk, float]]:
        """
        Generic scoped search implementation.

        1. Run a broad BM25 search to get many candidates.
        2. Filter candidates whose pre-computed flag matches.
        3. Also boost candidates whose titles contain any of the given keywords.
        4. If no flagged chunks exist, fall back to generic results.

        Heading weights and title boosts stack multiplicatively.
        """
        broad_results = self.search(query, top_k=top_k * 10)

        # Filter by pre-computed flags using O(1) chunk index lookup
        flagged = []
        for chunk, score in broad_results:
            chunk_idx = self._chunk_to_idx[id(chunk)]
            flags = self._chunk_flags[chunk_idx]

            # Check if the chunk matches the category
            if flags.get(flag_key, False):
                # Boost score if title also matches
                title_lower = chunk.title.lower()
                title_boost = any(kw in title_lower for kw in title_keywords)
                # Same per-chunk weight used by search(): heading weight with
                # prompt-index damping.  Identical to the heading weight for
                # every chunk that is not a prompt-index section.
                heading_weight = self._score_weights[chunk_idx]
                # Title boost and heading weight stack multiplicatively
                boosted_score = score * (1.5 if title_boost else 1.0) * heading_weight
                flagged.append((chunk, boosted_score))

        if flagged:
            # Re-sort by boosted score
            flagged.sort(key=lambda x: x[1], reverse=True)
            return flagged[:top_k]

        # Fallback: return generic results if no category matches
        return broad_results[:top_k]

    @staticmethod
    def _matches_keywords(text: str, keywords: frozenset[str]) -> bool:
        """Check if any keyword appears as a substring in the text."""
        return any(kw in text for kw in keywords)


# ---------------------------------------------------------------------------
# CLI: interactive search for development/testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from loader import MarkdownLoader

    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

    loader = MarkdownLoader("docs")
    chunks = loader.load()
    engine = SearchEngine(chunks)

    print(f"\n{'=' * 60}")
    print("  TeleBot Studio Search Engine — Interactive Mode")
    print(f"  {len(chunks)} chunks indexed")
    print(f"{'=' * 60}\n")

    while True:
        try:
            query = input("Search > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue

        if query.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        results = engine.search(query)
        if not results:
            print("\n  No results found.\n")
            continue

        print()
        for i, (chunk, score) in enumerate(results, start=1):
            print(f"  {i}. [{score:.3f}] {chunk.file} — {chunk.title}")
            print(f"     Level: H{chunk.heading_level}")
            print(f"     {chunk.content[:200].strip()}...")
            print()

        # Cache stats
        print(
            f"  (Cache: {engine.cache.hits} hits, "
            f"{engine.cache.misses} misses)\n"
        )
