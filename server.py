from __future__ import annotations

import argparse
import logging
from typing import List

from fastmcp import FastMCP

from loader import Chunk, MarkdownLoader
from search import SearchEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Build Search Engine
# --------------------------------------------------

def build_engine() -> SearchEngine:
    """
    Load all markdown files and build
    the BM25 search index.
    """

    loader = MarkdownLoader("docs")

    chunks = loader.load()

    logger.info("Loaded %d searchable chunks.", len(chunks))

    return SearchEngine(chunks)


engine = build_engine()


# --------------------------------------------------
# MCP Server
# --------------------------------------------------

mcp = FastMCP(
    name="TeleBot Studio MCP",
    instructions=(
        "Official TeleBot Studio documentation server. "
        "Always answer using the official documentation."
    ),
    version="1.0.0",
    website_url="https://help.telebotstudio.com",
)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def chunk_to_markdown(chunk: Chunk) -> str:
    """
    Convert a chunk into rich markdown.
    """

    return (
        f"# {chunk.title}\n\n"
        f"**File:** `{chunk.file}`\n\n"
        f"{chunk.content}"
    )


def chunks_to_markdown(chunks: List[Chunk]) -> str:

    if not chunks:
        return "No matching documentation found."

    parts: list[str] = []

    for chunk in chunks:

        parts.append(chunk_to_markdown(chunk))

    return "\n\n---\n\n".join(parts)


# --------------------------------------------------
# MCP Tools
# --------------------------------------------------


@mcp.tool
def search_docs(query: str, top_k: int = 5) -> str:
    """
    Search the TeleBot Studio documentation.
    """

    return chunks_to_markdown(
        engine.search(query, top_k)
    )


@mcp.tool
def get_page(name: str) -> str:
    """
    Return a complete markdown page.
    """

    return chunks_to_markdown(
        engine.get_page(name)
    )


@mcp.tool
def list_pages() -> list[str]:
    """
    List every available documentation page.
    """

    return engine.list_pages()


@mcp.tool
def search_examples(
    query: str,
    top_k: int = 5,
) -> str:
    """
    Search code examples.
    """

    return chunks_to_markdown(
        engine.search_examples(query, top_k)
    )


@mcp.tool
def search_api(
    query: str,
    top_k: int = 5,
) -> str:
    """
    Search API reference.
    """

    return chunks_to_markdown(
        engine.search_api(query, top_k)
    )


@mcp.tool
def search_library(
    query: str,
    top_k: int = 5,
) -> str:
    """
    Search TeleBot Studio libraries.
    """

    return chunks_to_markdown(
        engine.search(query, top_k)
    )


@mcp.tool
def search_functions(
    query: str,
    top_k: int = 5,
) -> str:
    """
    Search functions.
    """

    return chunks_to_markdown(
        engine.search(query, top_k)
    )


@mcp.tool
def search_errors(
    query: str,
    top_k: int = 5,
) -> str:
    """
    Search troubleshooting and errors.
    """

    return chunks_to_markdown(
        engine.search(query, top_k)
    )

# --------------------------------------------------
# Main
# --------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TeleBot Studio MCP Server"
    )

    parser.add_argument(
        "--transport",
        choices=[
            "stdio",
            "http",
        ],
        default="stdio",
        help="Transport type",
    )

    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="HTTP host",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP port",
    )

    args = parser.parse_args()

    logger.info("Transport: %s", args.transport)

    if args.transport == "stdio":
        mcp.run(
            transport="stdio",
        )

    else:
        mcp.run(
            transport="http",
            host=args.host,
            port=args.port,
            path="/mcp",
        )


if __name__ == "__main__":
    main()