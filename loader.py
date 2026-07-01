"""
Markdown documentation loader with heading-aware chunking.

Reads markdown files from the docs/ directory and splits them into
chunks based on heading boundaries (H1, H2, H3). This ensures
context is never arbitrarily broken in the middle of a thought
or API definition.

Chunking Strategy:
    We do NOT use arbitrary character counts (e.g., "split every 500
    tokens").  Arbitrary splits destroy context.  Instead, we parse
    the AST of the Markdown file and split exclusively on headings
    (#, ##, ###).  This guarantees every chunk contains a complete,
    self-contained thought or API definition.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Chunk:
    """A single searchable documentation chunk."""

    title: str
    file: str
    heading_level: int
    content: str

    def __str__(self) -> str:
        level_marker = "#" * self.heading_level if self.heading_level else ""
        return f"{level_marker} {self.title} ({self.file})"


class MarkdownLoader:
    """
    Loads markdown documentation files and splits them into
    heading-aware chunks.

    The loader respects code fences (```) so that headings inside
    code blocks are NOT treated as chunk boundaries.
    """

    # Only split on H1, H2, H3 to preserve context
    HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$")

    def __init__(self, docs_path: str = "docs") -> None:
        """
        Args:
            docs_path: Path to the directory containing .md files.
        """
        self.docs_path = Path(docs_path)

    def load(self) -> List[Chunk]:
        """
        Load all markdown files and return a list of chunks.

        Files are processed in sorted order for deterministic output.
        Empty or unreadable files are skipped with a warning.
        """
        if not self.docs_path.exists():
            logger.error("Documentation directory not found: %s", self.docs_path)
            return []

        if not self.docs_path.is_dir():
            logger.error("Documentation path is not a directory: %s", self.docs_path)
            return []

        files = sorted(self.docs_path.glob("*.md"))

        if not files:
            logger.warning("No markdown files found in %s", self.docs_path)
            return []

        logger.info("Found %d markdown files in %s", len(files), self.docs_path)

        chunks: List[Chunk] = []

        for file in files:
            try:
                file_chunks = self._parse_file(file)
                if file_chunks:
                    chunks.extend(file_chunks)
                    logger.debug("  %s: %d chunks", file.name, len(file_chunks))
                else:
                    logger.warning("  %s: no chunks produced (empty file?)", file.name)
            except Exception as e:
                logger.error("  %s: failed to parse: %s", file.name, e)

        logger.info("Created %d total chunks", len(chunks))

        return chunks

    def _parse_file(self, path: Path) -> List[Chunk]:
        """
        Parse a single markdown file into heading-aware chunks.

        The algorithm:
        1. Read the file line by line.
        2. Track whether we are inside a code fence.
        3. When we encounter a heading (H1-H3) outside a code fence,
           flush the current chunk and start a new one.
        4. After processing all lines, flush the final chunk.
        """
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            logger.error("Cannot read %s: %s", path, e)
            return []

        lines = text.splitlines()

        if not lines:
            return []

        chunks: List[Chunk] = []

        current_title = path.stem  # Default: filename without extension
        current_level = 0
        current_lines: List[str] = []

        inside_code = False
        code_fence_char = ""

        for line in lines:
            stripped = line.strip()

            # Track code fence state
            if stripped.startswith("```"):
                fence_char = stripped[:3]
                if not inside_code:
                    inside_code = True
                    code_fence_char = fence_char
                elif fence_char == code_fence_char:
                    inside_code = False
                    code_fence_char = ""
                # If fence chars don't match (unlikely but possible), keep state

            # Check for heading ONLY outside code fences
            if not inside_code:
                match = self.HEADING_RE.match(line)

                if match:
                    # Flush current chunk (if it has content)
                    if current_lines:
                        content = "\n".join(current_lines).strip()
                        if content:  # Skip empty chunks
                            chunks.append(
                                Chunk(
                                    title=current_title,
                                    file=path.name,
                                    heading_level=current_level,
                                    content=content,
                                )
                            )

                    # Start new chunk
                    current_level = len(match.group(1))
                    current_title = match.group(2).strip()
                    current_lines = [line]
                    continue

            current_lines.append(line)

        # Flush the final chunk
        if current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append(
                    Chunk(
                        title=current_title,
                        file=path.name,
                        heading_level=current_level,
                        content=content,
                    )
                )

        return chunks


# ---------------------------------------------------------------------------
# CLI: chunk inspection for development/testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    loader = MarkdownLoader(docs_dir)
    chunks = loader.load()

    print(f"\n{'=' * 60}")
    print(f"  TeleBot Studio Chunk Inspector")
    print(f"  {len(chunks)} chunks from '{docs_dir}/'")
    print(f"{'=' * 60}\n")

    # Show summary
    files = sorted({c.file for c in chunks})
    print(f"Files ({len(files)}):")
    for f in files:
        count = sum(1 for c in chunks if c.file == f)
        print(f"  - {f} ({count} chunks)")
    print()

    # Show first N chunks
    limit = 20
    for i, chunk in enumerate(chunks[:limit]):
        print(f"[{i + 1}] H{chunk.heading_level} | {chunk.file} | {chunk.title}")
        preview = chunk.content[:150].replace("\n", " ")
        print(f"    {preview}...")
        print()

    if len(chunks) > limit:
        print(f"  ... and {len(chunks) - limit} more chunks")
