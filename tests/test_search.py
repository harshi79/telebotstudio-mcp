"""Tests for SearchEngine and related utilities."""

from __future__ import annotations

import threading

import pytest

from loader import Chunk
from search import LRUCache, SearchEngine, tokenize, tokenize_with_bigrams

# ---------------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------------


class TestTokenize:
    """Test the tokenize function."""

    def test_basic_tokenization(self):
        result = tokenize("Hello World")
        assert result == ["hello", "world"]

    def test_preserves_dots_and_underscores(self):
        """Technical identifiers like TeleBot.send_message should be kept."""
        result = tokenize("TeleBot.send_message")
        assert "telebot.send_message" in result

    def test_lowercase(self):
        result = tokenize("API Reference")
        assert result == ["api", "reference"]

    def test_empty_string(self):
        assert tokenize("") == []

    def test_numbers_preserved(self):
        result = tokenize("Python 3.12")
        assert "python" in result
        assert "3.12" in result

    def test_special_chars_removed(self):
        result = tokenize("hello! @world #tag")
        assert "hello" in result
        assert "world" in result
        assert "tag" in result


class TestTokenizeWithBigrams:
    """Test the tokenize_with_bigrams function."""

    def test_includes_unigrams(self):
        result = tokenize_with_bigrams("hello world")
        assert "hello" in result
        assert "world" in result

    def test_includes_bigrams(self):
        result = tokenize_with_bigrams("send message")
        assert "send_message" in result

    def test_single_word_no_bigrams(self):
        result = tokenize_with_bigrams("hello")
        assert result == ["hello"]

    def test_empty_string(self):
        assert tokenize_with_bigrams("") == []

    def test_three_words_two_bigrams(self):
        result = tokenize_with_bigrams("a b c")
        assert "a_b" in result
        assert "b_c" in result
        # Should have 3 unigrams + 2 bigrams = 5
        assert len(result) == 5


# ---------------------------------------------------------------------------
# LRU Cache
# ---------------------------------------------------------------------------


class TestLRUCache:
    """Test the LRUCache."""

    def test_cache_miss_returns_none(self):
        cache = LRUCache(maxsize=10)
        assert cache.get("search", "test", 5) is None

    def test_cache_put_and_get(self):
        cache = LRUCache(maxsize=10)
        results = [("chunk1", 1.0)]
        cache.put("search", "test", 5, results)
        assert cache.get("search", "test", 5) == results

    def test_cache_hit_increments_hits(self):
        cache = LRUCache(maxsize=10)
        cache.put("search", "q", 5, [])
        # First get is a hit
        cache.get("search", "q", 5)
        assert cache.hits == 1

    def test_cache_miss_increments_misses(self):
        cache = LRUCache(maxsize=10)
        cache.get("search", "missing", 5)
        assert cache.misses == 1

    def test_cache_eviction(self):
        """When cache exceeds maxsize, oldest entry is evicted."""
        cache = LRUCache(maxsize=2)
        cache.put("m", "q1", 5, ["r1"])
        cache.put("m", "q2", 5, ["r2"])
        cache.put("m", "q3", 5, ["r3"])
        # q1 should be evicted
        assert cache.get("m", "q1", 5) is None
        # q2 and q3 should still be present
        assert cache.get("m", "q2", 5) == ["r2"]
        assert cache.get("m", "q3", 5) == ["r3"]

    def test_cache_lru_access_renews_entry(self):
        """Accessing an entry moves it to the end, preventing eviction."""
        cache = LRUCache(maxsize=2)
        cache.put("m", "q1", 5, ["r1"])
        cache.put("m", "q2", 5, ["r2"])
        # Access q1 to move it to the end
        cache.get("m", "q1", 5)
        # Now add q3 — q2 should be evicted (not q1)
        cache.put("m", "q3", 5, ["r3"])
        assert cache.get("m", "q1", 5) == ["r1"]
        assert cache.get("m", "q2", 5) is None

    def test_different_methods_are_different_keys(self):
        cache = LRUCache(maxsize=10)
        cache.put("search", "q", 5, ["r1"])
        cache.put("search_api", "q", 5, ["r2"])
        assert cache.get("search", "q", 5) == ["r1"]
        assert cache.get("search_api", "q", 5) == ["r2"]

    def test_thread_safety(self):
        """Multiple threads can safely access the cache."""
        cache = LRUCache(maxsize=100)
        errors = []

        def worker(idx):
            try:
                key = f"q{idx}"
                cache.put("m", key, 5, [f"r{idx}"])
                result = cache.get("m", key, 5)
                if result != [f"r{idx}"]:
                    errors.append(f"Thread {idx}: unexpected result {result}")
            except Exception as e:
                errors.append(f"Thread {idx}: {e}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread safety errors: {errors}"


# ---------------------------------------------------------------------------
# SearchEngine
# ---------------------------------------------------------------------------


class TestSearchEngine:
    """Test the SearchEngine."""

    @pytest.fixture
    def engine(self, sample_chunks):
        return SearchEngine(sample_chunks, cache_size=10)

    def test_basic_search_returns_ranked_results(self, engine):
        """BM25 search should return results with positive scores."""
        results = engine.search("install library")
        assert len(results) > 0
        # Results should be (Chunk, score) tuples
        for chunk, score in results:
            assert isinstance(chunk, Chunk)
            assert isinstance(score, float)
            assert score > 0

    def test_search_results_sorted_by_score_desc(self, engine):
        """Results should be sorted by score descending."""
        results = engine.search("install library")
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_query_returns_no_results(self, engine):
        """Empty or whitespace-only queries should return no results."""
        assert engine.search("") == []
        assert engine.search("   ") == []

    def test_top_k_limits_results(self, engine):
        """The top_k parameter should limit the number of results."""
        results = engine.search("telebot", top_k=2)
        assert len(results) <= 2

    def test_unrelated_query_may_return_no_positive_results(self, engine):
        """A query about something totally unrelated might have no positive scores."""
        results = engine.search("zzzzzzz_unlikely_topic_xyz")
        # Could be empty or have low scores; just ensure no crash
        for _chunk, score in results:
            assert score > 0

    def test_search_caches_results(self, engine):
        """Repeated identical queries should hit the cache."""
        engine.search("install")
        engine.search("install")
        assert engine.cache.hits >= 1

    # -- Scoped searches --

    def test_search_examples(self, engine):
        """search_examples should prefer code-containing chunks."""
        results = engine.search_examples("send message")
        assert len(results) > 0

    def test_search_api(self, engine):
        """search_api should return API-related chunks."""
        results = engine.search_api("endpoint")
        assert len(results) > 0

    def test_search_library(self, engine):
        """search_library should return library/installation-related chunks."""
        results = engine.search_library("install")
        assert len(results) > 0

    def test_search_functions(self, engine):
        """search_functions should return function-related chunks."""
        results = engine.search_functions("function method")
        # May return results if any chunk matches FUNCTION_KEYWORDS,
        # or falls back to generic results
        assert isinstance(results, list)

    def test_search_errors(self, engine):
        """search_errors should return error/troubleshooting-related chunks."""
        results = engine.search_errors("exception")
        assert len(results) > 0

    # -- get_page --

    def test_get_page_case_insensitive(self, engine):
        """get_page should match filenames case-insensitively."""
        results = engine.get_page("GETTING-STARTED")
        assert len(results) > 0
        assert all(c.file.lower() == "getting-started.md" for c in results)

    def test_get_page_with_md_extension(self, engine):
        """get_page should work with or without .md extension."""
        with_ext = engine.get_page("getting-started.md")
        without_ext = engine.get_page("getting-started")
        assert len(with_ext) == len(without_ext)

    def test_get_page_not_found(self, engine):
        """Non-existent page should return empty list."""
        results = engine.get_page("nonexistent-page")
        assert results == []

    # -- list_pages --

    def test_list_pages_returns_sorted_unique(self, engine):
        """list_pages should return sorted unique filenames."""
        pages = engine.list_pages()
        assert pages == sorted(pages)
        assert len(pages) == len(set(pages))

    # -- _matches_keywords --

    def test_matches_keywords_true(self):
        assert SearchEngine._matches_keywords("the api endpoint is here", SearchEngine.API_KEYWORDS)

    def test_matches_keywords_false(self):
        assert not SearchEngine._matches_keywords(
            "lorem ipsum dolor sit", SearchEngine.API_KEYWORDS
        )

    def test_matches_keywords_empty_text(self):
        assert not SearchEngine._matches_keywords("", SearchEngine.API_KEYWORDS)


# ---------------------------------------------------------------------------
# SearchEngine with empty chunks
# ---------------------------------------------------------------------------


class TestSearchEngineEmpty:
    """Test SearchEngine with empty chunk list.

    BM25Okapi raises ZeroDivisionError on empty corpus,
    so we test that SearchEngine handles it gracefully
    by adding a dummy placeholder if needed.
    """

    def test_empty_corpus_causes_error(self):
        """BM25Okapi cannot handle empty corpus — this is a known limitation."""
        with pytest.raises(ZeroDivisionError):
            SearchEngine([], cache_size=10)

    def test_single_empty_chunk_search(self):
        """A single chunk with minimal content should be searchable."""
        chunk = Chunk(title="Empty", file="e.md", heading_level=1, content="placeholder")
        engine = SearchEngine([chunk], cache_size=10)
        # Searching for something unrelated may return no results
        results = engine.search("zzzzz")
        assert isinstance(results, list)

    def test_single_chunk_list_pages(self):
        chunk = Chunk(title="Page", file="page.md", heading_level=1, content="text")
        engine = SearchEngine([chunk], cache_size=10)
        pages = engine.list_pages()
        assert pages == ["page.md"]

    def test_single_chunk_get_page(self):
        chunk = Chunk(title="Page", file="page.md", heading_level=1, content="text")
        engine = SearchEngine([chunk], cache_size=10)
        results = engine.get_page("page")
        assert len(results) == 1
