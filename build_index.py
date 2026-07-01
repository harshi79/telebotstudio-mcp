"""
Index builder and diagnostic tool for TeleBot Studio MCP.

This utility allows you to:
  - Build the BM25 search index from the docs/ directory
  - Verify that all documentation files load correctly
  - Run test searches against the index
  - Display index statistics and chunk details
  - Validate the entire pipeline before starting the server

Usage:
  python build_index.py                          # Build & show stats
  python build_index.py --search "send message"  # Test a search query
  python build_index.py --list                   # List all pages
  python build_index.py --page getting-started   # Show a specific page
  python build_index.py --validate               # Validate all chunks
  python build_index.py --verbose                # Show detailed chunk info
"""

from __future__ import annotations

import argparse
import logging
import sys
import time

from loader import MarkdownLoader
from search import SearchEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("build_index")


def build_and_validate(docs_dir: str) -> SearchEngine:
    """Build the search engine and validate the index."""
    start = time.time()
    loader = MarkdownLoader(docs_dir)
    chunks = loader.load()

    if not chunks:
        logger.error("No chunks loaded! Check your docs/ directory.")
        sys.exit(1)

    engine = SearchEngine(chunks)
    elapsed = time.time() - start

    logger.info("Index built in %.2f seconds", elapsed)
    return engine


def show_stats(engine: SearchEngine) -> None:
    """Display index statistics."""
    chunks = engine.chunks
    pages = engine.list_pages()
    flags = engine.chunk_flags  # Public property
    cache = engine.cache  # Public property

    print(f"\n{'=' * 60}")
    print("  TeleBot Studio MCP — Index Statistics")
    print(f"{'=' * 60}")
    print(f"  Total chunks:     {len(chunks)}")
    print(f"  Total pages:      {len(pages)}")
    print(f"  Cache max size:   {cache.maxsize}")

    # Content stats
    total_chars = sum(len(c.content) for c in chunks)
    avg_chunk_size = total_chars / len(chunks) if chunks else 0
    print(f"  Total content:    {total_chars:,} characters")
    print(f"  Avg chunk size:   {avg_chunk_size:.0f} characters")

    # Heading level distribution
    level_counts: dict[int, int] = {}
    for chunk in chunks:
        level_counts[chunk.heading_level] = level_counts.get(chunk.heading_level, 0) + 1

    print("\n  Heading Level Distribution:")
    for level in sorted(level_counts):
        label = {0: "Root", 1: "H1", 2: "H2", 3: "H3"}.get(level, f"H{level}")
        bar = "█" * (level_counts[level] // max(1, len(chunks) // 50))
        print(f"    {label:>4} ({level}): {level_counts[level]:>4}  {bar}")

    # Category breakdown
    code_count = sum(1 for f in flags if f["has_code"])
    api_count = sum(1 for f in flags if f["is_api"])
    lib_count = sum(1 for f in flags if f["is_library"])
    func_count = sum(1 for f in flags if f["is_function"])
    error_count = sum(1 for f in flags if f["is_error"])

    print("\n  Category Breakdown:")
    print(f"    Code examples:  {code_count}")
    print(f"    API reference:  {api_count}")
    print(f"    Library info:   {lib_count}")
    print(f"    Function defs:  {func_count}")
    print(f"    Error/trouble:  {error_count}")

    # Pages list
    print("\n  Available Pages:")
    for page in pages:
        chunk_count = sum(1 for c in chunks if c.file == page)
        print(f"    {page} ({chunk_count} chunks)")

    print(f"{'=' * 60}\n")


def run_search(engine: SearchEngine, query: str, top_k: int = 5) -> None:
    """Run a test search and display results."""
    print(f"\n  Searching: '{query}' (top {top_k})\n")

    results = engine.search(query, top_k)

    if not results:
        print("  No results found.")
        return

    for i, (chunk, score) in enumerate(results, start=1):
        print(f"  {i}. [score: {score:.3f}] {chunk.file}")
        print(f"     Heading: H{chunk.heading_level} — {chunk.title}")
        preview = chunk.content[:200].replace("\n", " ")
        print(f"     Preview: {preview}...")
        print()


def run_scoped_search(
    engine: SearchEngine,
    scope: str,
    query: str,
    top_k: int = 5,
) -> None:
    """Run a scoped test search."""
    method_map = {
        "examples": engine.search_examples,
        "api": engine.search_api,
        "library": engine.search_library,
        "functions": engine.search_functions,
        "errors": engine.search_errors,
    }

    if scope not in method_map:
        print(f"  Unknown scope: {scope}. Use: {', '.join(method_map)}")
        return

    print(f"\n  Scoped search [{scope}]: '{query}' (top {top_k})\n")

    results = method_map[scope](query, top_k)

    if not results:
        print("  No results found.")
        return

    for i, (chunk, score) in enumerate(results, start=1):
        print(f"  {i}. [score: {score:.3f}] {chunk.file}")
        print(f"     Heading: H{chunk.heading_level} — {chunk.title}")
        preview = chunk.content[:200].replace("\n", " ")
        print(f"     Preview: {preview}...")
        print()


def show_page(engine: SearchEngine, name: str) -> None:
    """Display a specific page's chunks."""
    chunks = engine.get_page(name)

    if not chunks:
        print(f"\n  Page not found: '{name}'")
        print("  Use --list to see available pages.")
        return

    print(f"\n  Page: {chunks[0].file} ({len(chunks)} sections)\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"  --- Section {i}: H{chunk.heading_level} {chunk.title} ---")
        print(f"  {chunk.content[:500]}")
        print()


def validate_chunks(engine: SearchEngine) -> bool:
    """Validate all chunks for potential issues."""
    issues = []

    for i, chunk in enumerate(engine.chunks):
        # Check for empty content
        if not chunk.content.strip():
            issues.append(f"  Chunk {i} ({chunk.file}/{chunk.title}): empty content")

        # Check for very short content (likely incomplete)
        if len(chunk.content.strip()) < 20:
            issues.append(
                f"  Chunk {i} ({chunk.file}/{chunk.title}): very short content "
                f"({len(chunk.content)} chars)"
            )

        # Check for missing title
        if not chunk.title.strip():
            issues.append(f"  Chunk {i} ({chunk.file}): missing title")

        # Check for unclosed code fences
        fence_count = chunk.content.count("```")
        if fence_count % 2 != 0:
            issues.append(
                f"  Chunk {i} ({chunk.file}/{chunk.title}): unclosed code fence"
            )

    if issues:
        print(f"\n  ⚠ Found {len(issues)} potential issues:\n")
        for issue in issues:
            print(issue)
        return False

    print(f"\n  ✓ All {len(engine.chunks)} chunks validated successfully.")
    return True


def show_verbose(engine: SearchEngine) -> None:
    """Show detailed chunk information."""
    flags = engine.chunk_flags  # Public property

    print(f"\n  All {len(engine.chunks)} chunks:\n")

    for i, chunk in enumerate(engine.chunks):
        chunk_flags = flags[i]
        tags = []
        if chunk_flags["has_code"]:
            tags.append("code")
        if chunk_flags["is_api"]:
            tags.append("api")
        if chunk_flags["is_library"]:
            tags.append("lib")
        if chunk_flags["is_function"]:
            tags.append("func")
        if chunk_flags["is_error"]:
            tags.append("err")

        tag_str = " ".join(f"[{t}]" for t in tags) if tags else "[general]"
        print(f"  {i + 1:>3}. H{chunk.heading_level} | {chunk.file} | {chunk.title} {tag_str}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TeleBot Studio MCP — Index Builder & Diagnostic Tool",
    )

    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="Path to documentation directory (default: docs)",
    )

    parser.add_argument(
        "--search",
        metavar="QUERY",
        help="Run a test search query",
    )

    parser.add_argument(
        "--scope",
        choices=["examples", "api", "library", "functions", "errors"],
        help="Scope for the search query",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of search results (default: 5)",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available pages",
    )

    parser.add_argument(
        "--page",
        metavar="NAME",
        help="Show chunks for a specific page",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate all chunks for potential issues",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed chunk information",
    )

    args = parser.parse_args()

    engine = build_and_validate(args.docs_dir)

    # Always show stats
    show_stats(engine)

    # Handle commands
    if args.search:
        if args.scope:
            run_scoped_search(engine, args.scope, args.search, args.top_k)
        else:
            run_search(engine, args.search, args.top_k)

    if args.list:
        pages = engine.list_pages()
        print(f"\n  Available Pages ({len(pages)}):\n")
        for page in pages:
            print(f"    {page}")
        print()

    if args.page:
        show_page(engine, args.page)

    if args.validate:
        validate_chunks(engine)

    if args.verbose:
        show_verbose(engine)

    # Cache stats
    cache = engine.cache  # Public property
    print(
        f"  Cache stats: {cache.hits} hits, "
        f"{cache.misses} misses"
    )


if __name__ == "__main__":
    main()
