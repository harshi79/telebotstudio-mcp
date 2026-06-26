from __future__ import annotations

import re
from typing import List

from rank_bm25 import BM25Okapi

from loader import Chunk


def tokenize(text: str) -> list[str]:
    """
    Convert text into searchable tokens.
    """
    return re.findall(r"[a-zA-Z0-9_.]+", text.lower())


class SearchEngine:
    """
    BM25-based search engine for markdown chunks.
    """

    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks

        self.corpus = [
            tokenize(
                f"{chunk.title}\n{chunk.content}"
            )
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(self.corpus)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Chunk]:
        """
        Search documentation.
        """

        tokens = tokenize(query)

        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.chunks),
            key=lambda x: x[0],
            reverse=True,
        )

        results: List[Chunk] = []

        for score, chunk in ranked:
            if score <= 0:
                continue

            results.append(chunk)

            if len(results) >= top_k:
                break

        return results

    def get_page(self, filename: str) -> List[Chunk]:
        """
        Return all chunks belonging to one markdown file.
        """

        filename = filename.lower()

        return [
            chunk
            for chunk in self.chunks
            if chunk.file.lower() == filename
            or chunk.file.lower() == filename + ".md"
        ]

    def list_pages(self) -> List[str]:
        """
        Return all markdown files.
        """

        return sorted(
            {
                chunk.file
                for chunk in self.chunks
            }
        )

    def search_examples(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Chunk]:
        """
        Prefer chunks containing code blocks.
        """

        results = self.search(query, top_k=50)

        code = [
            chunk
            for chunk in results
            if "```" in chunk.content
        ]

        if code:
            return code[:top_k]

        return results[:top_k]

    def search_api(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Chunk]:
        """
        Prefer API/function reference chunks.
        """

        results = self.search(query, top_k=50)

        api = [
            chunk
            for chunk in results
            if (
                "api" in chunk.title.lower()
                or "function" in chunk.title.lower()
                or "method" in chunk.title.lower()
                or "library" in chunk.title.lower()
            )
        ]

        if api:
            return api[:top_k]

        return results[:top_k]


if __name__ == "__main__":

    from loader import MarkdownLoader

    loader = MarkdownLoader("docs")

    chunks = loader.load()

    engine = SearchEngine(chunks)

    print("\n===== Search Results =====\n")

    query = input("Search > ")

    results = engine.search(query)

    if not results:
        print("\nNo results found.")
        raise SystemExit

    for i, chunk in enumerate(results, start=1):
        print("=" * 80)
        print(f"{i}. {chunk.file}")
        print(f"Title : {chunk.title}")
        print(f"Level : H{chunk.heading_level}")
        print("-" * 80)
        print(chunk.content[:700])
        print()