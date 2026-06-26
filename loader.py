from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Chunk:
    title: str
    file: str
    heading_level: int
    content: str


class MarkdownLoader:
    HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")

    def __init__(self, docs_path: str = "docs"):
        self.docs_path = Path(docs_path)

    def load(self) -> list[Chunk]:
        chunks: list[Chunk] = []

        files = sorted(self.docs_path.glob("*.md"))

        logger.info("Found %d markdown files", len(files))

        for file in files:
            chunks.extend(self._parse_file(file))

        logger.info("Created %d chunks", len(chunks))

        return chunks

    def _parse_file(self, path: Path) -> list[Chunk]:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        lines = text.splitlines()

        chunks: list[Chunk] = []

        current_title = path.stem
        current_level = 0
        current_lines: list[str] = []

        inside_code = False

        for line in lines:

            if line.strip().startswith("```"):
                inside_code = not inside_code

            if not inside_code:
                match = self.HEADING_RE.match(line)

                if match:

                    if current_lines:
                        chunks.append(
                            Chunk(
                                title=current_title,
                                file=path.name,
                                heading_level=current_level,
                                content="\n".join(current_lines).strip(),
                            )
                        )

                    current_level = len(match.group(1))
                    current_title = match.group(2).strip()
                    current_lines = [line]
                    continue

            current_lines.append(line)

        if current_lines:
            chunks.append(
                Chunk(
                    title=current_title,
                    file=path.name,
                    heading_level=current_level,
                    content="\n".join(current_lines).strip(),
                )
            )

        return chunks


if __name__ == "__main__":
    loader = MarkdownLoader("docs")
    chunks = loader.load()

    print(f"\nLoaded {len(chunks)} chunks\n")

    for chunk in chunks[:15]:
        print(f"[L{chunk.heading_level}] {chunk.file} -> {chunk.title}")