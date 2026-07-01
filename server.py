"""
TeleBot Studio MCP Server.

Production-ready Model Context Protocol server that indexes official
TeleBot Studio documentation via deterministic BM25 ranking.
Zero embeddings. Zero external APIs.

Supports:
  - STDIO transport (Claude Desktop, Cursor, etc.)
  - HTTP / Streamable HTTP transport (remote clients, web dashboards)

Usage:
  python server.py                                  # STDIO mode (default)
  python server.py --transport http                 # HTTP mode on port 8000
  python server.py --transport http --port 9000     # HTTP mode on custom port
  python server.py --transport http --host 0.0.0.0 --port 9000
  python server.py --docs-dir /path/to/docs         # Custom docs directory
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from loader import Chunk, MarkdownLoader
from search import SearchEngine

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("telebotstudio-mcp")


# ---------------------------------------------------------------------------
# Build Search Engine
# ---------------------------------------------------------------------------

DOCS_DIR = os.environ.get("TBS_DOCS_DIR", "docs")

# Maximum allowed query length to prevent resource exhaustion
MAX_QUERY_LENGTH = 500


class ConfigurationError(Exception):
    """Raised when the server cannot be configured properly."""


def build_engine(docs_dir: str = DOCS_DIR) -> SearchEngine:
    """
    Load all markdown files from the docs directory and build
    the BM25 search index.

    The index is built once at startup and kept in memory for
    zero cold-start latency on subsequent queries.

    Raises:
        ConfigurationError: If the docs directory is missing or empty.
    """
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise ConfigurationError(
            f"Documentation directory not found: {docs_path}"
        )

    if not docs_path.is_dir():
        raise ConfigurationError(
            f"Documentation path is not a directory: {docs_path}"
        )

    loader = MarkdownLoader(docs_dir)
    chunks = loader.load()

    if not chunks:
        raise ConfigurationError(
            f"No documentation chunks loaded from {docs_path}. "
            "Ensure the docs/ directory contains .md files."
        )

    logger.info("Loaded %d searchable chunks from %s", len(chunks), docs_dir)

    return SearchEngine(chunks)


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="TeleBot Studio MCP",
    instructions=(
        "Official TeleBot Studio documentation server. "
        "Always answer using the official documentation. "
        "Use search_docs for general queries, and scoped tools "
        "(search_examples, search_api, search_library, search_functions, "
        "search_errors) for targeted searches. Use get_page to retrieve "
        "an entire documentation page, and list_pages to see all available pages."
    ),
)


# ---------------------------------------------------------------------------
# Health Endpoint (for uptime monitoring, e.g. UptimeRobot)
# ---------------------------------------------------------------------------

@mcp.custom_route("/health", methods=["GET"], name="health_check")
async def health_check(request: Request) -> Response:
    """Lightweight health endpoint for uptime monitoring tools."""
    return JSONResponse({"status": "ok"})

# Engine is initialized lazily so --docs-dir can take effect
_engine: SearchEngine | None = None
_engine_docs_dir: str | None = None


def get_engine() -> SearchEngine:
    """Get or initialize the search engine."""
    global _engine, _engine_docs_dir
    if _engine is None:
        docs_dir = _engine_docs_dir or DOCS_DIR
        _engine = build_engine(docs_dir)
    return _engine


def set_docs_dir(docs_dir: str) -> None:
    """Set the docs directory for engine initialization."""
    global _engine_docs_dir
    _engine_docs_dir = docs_dir


# ---------------------------------------------------------------------------
# Response Formatting
# ---------------------------------------------------------------------------

def _format_chunk_result(chunk: Chunk, score: float) -> Dict[str, Any]:
    """Format a single chunk into a structured result dict."""
    return {
        "score": round(score, 3),
        "source": chunk.file,
        "heading": chunk.title,
        "heading_level": chunk.heading_level,
        "content": chunk.content,
    }


def _format_results(chunks_with_scores: List[Tuple[Chunk, float]]) -> str:
    """
    Format search results as structured JSON.

    Returns JSON with a "results" array containing matched chunks,
    each with score, source file, heading, heading_level, and content.
    """
    if not chunks_with_scores:
        return json.dumps(
            {"results": [], "message": "No matching documentation found."},
            indent=2,
        )

    results = [_format_chunk_result(chunk, score) for chunk, score in chunks_with_scores]
    return json.dumps({"results": results}, indent=2)


def _format_page_chunks(chunks: List[Chunk]) -> str:
    """Format page retrieval results as structured JSON."""
    if not chunks:
        return json.dumps(
            {"results": [], "message": "Page not found. Use list_pages to see available pages."},
            indent=2,
        )

    page_name = chunks[0].file
    full_content = "\n\n".join(chunk.content for chunk in chunks)
    sections = [
        {
            "heading": chunk.title,
            "heading_level": chunk.heading_level,
            "content": chunk.content,
        }
        for chunk in chunks
    ]

    return json.dumps(
        {
            "page": page_name,
            "sections": sections,
            "full_content": full_content,
        },
        indent=2,
    )


# ---------------------------------------------------------------------------
# Input Validation
# ---------------------------------------------------------------------------

def _validate_query(query: str) -> str:
    """Validate and clean a search query string."""
    if not query or not query.strip():
        raise ValueError("Query must not be empty.")
    cleaned = query.strip()
    if len(cleaned) > MAX_QUERY_LENGTH:
        raise ValueError(
            f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters."
        )
    return cleaned


def _validate_top_k(top_k: int) -> int:
    """Validate the top_k parameter."""
    if not isinstance(top_k, int):
        raise ValueError("top_k must be an integer.")
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")
    if top_k > 50:
        raise ValueError("top_k must be at most 50.")
    return top_k


def _validate_name(name: str) -> str:
    """
    Validate a page name and prevent path traversal.

    Only allows alphanumeric characters, hyphens, underscores, and dots.
    Rejects names that could resolve to paths outside the docs directory.
    """
    if not name or not name.strip():
        raise ValueError("Page name must not be empty.")

    cleaned = name.strip()

    # Use a strict allowlist: only safe filename characters
    # This prevents path traversal more robustly than stripping bad chars
    safe_name = "".join(
        c for c in cleaned
        if c.isalnum() or c in "-_."
    )

    if not safe_name:
        raise ValueError("Page name contains no valid characters.")

    # Additional safety: ensure no path-like patterns remain
    if "/" in safe_name or "\\" in safe_name or ".." in safe_name:
        raise ValueError("Page name contains invalid path characters.")

    return safe_name


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool
def search_docs(query: str, top_k: int = 5) -> str:
    """
    Search the TeleBot Studio documentation using BM25 ranking.

    This is the primary tool for full-text search across all
    documentation chunks. Returns the top ranked results with
    relevance scores.

    Args:
        query: The search query string. Can contain function names,
               error messages, concepts, or any documentation topic.
        top_k: Number of results to return (1-50, default 5).

    Returns:
        JSON object with a "results" array containing matched chunks,
        each with score, source file, heading, and content.
    """
    try:
        query = _validate_query(query)
        top_k = _validate_top_k(top_k)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    engine = get_engine()
    logger.info("search_docs: query=%r top_k=%d", query, top_k)
    results = engine.search(query, top_k)
    return _format_results(results)


@mcp.tool
def get_page(name: str) -> str:
    """
    Retrieve all sections of a specific documentation page by its filename.

    Returns the page's sections (headings and content) as well as the
    full concatenated page content.

    Args:
        name: The markdown filename (e.g., "getting-started.md" or
              "getting-started"). Case-insensitive.

    Returns:
        JSON object with the page filename, all sections, and the
        full concatenated content.
    """
    try:
        name = _validate_name(name)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    engine = get_engine()
    logger.info("get_page: name=%r", name)
    chunks = engine.get_page(name)
    return _format_page_chunks(chunks)


@mcp.tool
def list_pages() -> str:
    """
    Returns a complete list of all available documentation pages,
    filenames, and total count.

    Returns:
        JSON object with a "pages" array of all available markdown
        filenames in the documentation corpus.
    """
    engine = get_engine()
    logger.info("list_pages")
    pages = engine.list_pages()
    return json.dumps(
        {
            "pages": pages,
            "total": len(pages),
        },
        indent=2,
    )


@mcp.tool
def search_examples(query: str, top_k: int = 5) -> str:
    """
    Scoped search targeting exclusively code examples and usage
    snippets. Preferentially returns chunks containing code blocks
    (fenced with ```).

    Args:
        query: The search query. Use function names, patterns, or
               concepts to find relevant code examples.
        top_k: Number of results to return (1-50, default 5).

    Returns:
        JSON object with a "results" array of code-example-rich chunks.
    """
    try:
        query = _validate_query(query)
        top_k = _validate_top_k(top_k)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    engine = get_engine()
    logger.info("search_examples: query=%r top_k=%d", query, top_k)
    results = engine.search_examples(query, top_k)
    return _format_results(results)


@mcp.tool
def search_api(query: str, top_k: int = 5) -> str:
    """
    Scoped search restricted to API references, endpoints, and
    configuration parameters. Targets chunks that describe APIs,
    methods, classes, and configuration options.

    Args:
        query: The search query. Use API names, endpoint paths,
               or configuration keys.
        top_k: Number of results to return (1-50, default 5).

    Returns:
        JSON object with a "results" array of API-related chunks.
    """
    try:
        query = _validate_query(query)
        top_k = _validate_top_k(top_k)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    engine = get_engine()
    logger.info("search_api: query=%r top_k=%d", query, top_k)
    results = engine.search_api(query, top_k)
    return _format_results(results)


@mcp.tool
def search_library(query: str, top_k: int = 5) -> str:
    """
    Search for library installations, imports, and third-party
    dependency information. Targets chunks about installing,
    configuring, and managing libraries and packages.

    Args:
        query: The search query. Use library names, import
               statements, or package-related terms.
        top_k: Number of results to return (1-50, default 5).

    Returns:
        JSON object with a "results" array of library-related chunks.
    """
    try:
        query = _validate_query(query)
        top_k = _validate_top_k(top_k)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    engine = get_engine()
    logger.info("search_library: query=%r top_k=%d", query, top_k)
    results = engine.search_library(query, top_k)
    return _format_results(results)


@mcp.tool
def search_functions(query: str, top_k: int = 5) -> str:
    """
    Targeted search for specific function definitions, signatures,
    and method explanations. Returns chunks that describe callable
    functions, methods, callbacks, and decorators.

    Args:
        query: The search query. Use function or method names,
               signatures, or behavior descriptions.
        top_k: Number of results to return (1-50, default 5).

    Returns:
        JSON object with a "results" array of function-related chunks.
    """
    try:
        query = _validate_query(query)
        top_k = _validate_top_k(top_k)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    engine = get_engine()
    logger.info("search_functions: query=%r top_k=%d", query, top_k)
    results = engine.search_functions(query, top_k)
    return _format_results(results)


@mcp.tool
def search_errors(query: str, top_k: int = 5) -> str:
    """
    Search for error codes, exception handling, troubleshooting
    guides, and common pitfalls. Targets chunks that describe
    errors, exceptions, debugging steps, and fixes.

    Args:
        query: The search query. Use error messages, exception
               names, or troubleshooting terms.
        top_k: Number of results to return (1-50, default 5).

    Returns:
        JSON object with a "results" array of error-related chunks.
    """
    try:
        query = _validate_query(query)
        top_k = _validate_top_k(top_k)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    engine = get_engine()
    logger.info("search_errors: query=%r top_k=%d", query, top_k)
    results = engine.search_errors(query, top_k)
    return _format_results(results)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TeleBot Studio MCP Server — "
        "BM25-powered documentation search via Model Context Protocol",
    )

    parser.add_argument(
        "--transport",
        choices=[
            "stdio",
            "http",
        ],
        default="stdio",
        help="Transport type: 'stdio' for Claude Desktop / Cursor, "
             "'http' for remote clients and web dashboards (default: stdio)",
    )

    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", "0.0.0.0"),
        help="HTTP host to bind to (default: 0.0.0.0, respects HOST env var)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "8000")),
        help="HTTP port to listen on (default: 8000, respects PORT env var)",
    )

    parser.add_argument(
        "--docs-dir",
        default=DOCS_DIR,
        help="Path to the documentation directory (default: docs/)",
    )

    args = parser.parse_args()

    # Set docs directory before engine initialization
    set_docs_dir(args.docs_dir)

    logger.info("Starting TeleBot Studio MCP Server")
    logger.info("Transport: %s", args.transport)
    logger.info("Docs directory: %s", args.docs_dir)

    # Initialize engine (will raise ConfigurationError on failure)
    try:
        get_engine()
    except ConfigurationError as e:
        logger.error("Configuration error: %s", e)
        sys.exit(1)

    if args.transport == "http":
        logger.info("Host: %s | Port: %d", args.host, args.port)
        logger.info("MCP endpoint: http://%s:%d/mcp", args.host, args.port)

    try:
        if args.transport == "stdio":
            mcp.run(transport="stdio")
        else:
            mcp.run(
                transport="streamable-http",
                host=args.host,
                port=args.port,
                path="/mcp",
            )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
