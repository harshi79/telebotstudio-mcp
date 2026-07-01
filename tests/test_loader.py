"""Tests for MarkdownLoader and Chunk dataclass."""

from __future__ import annotations

from loader import Chunk, MarkdownLoader

# ---------------------------------------------------------------------------
# Chunk dataclass
# ---------------------------------------------------------------------------


class TestChunk:
    """Test the Chunk dataclass."""

    def test_chunk_creation(self):
        chunk = Chunk(
            title="Test Title",
            file="test.md",
            heading_level=2,
            content="Some content here.",
        )
        assert chunk.title == "Test Title"
        assert chunk.file == "test.md"
        assert chunk.heading_level == 2
        assert chunk.content == "Some content here."

    def test_chunk_str_with_heading_level(self):
        chunk = Chunk(title="My Section", file="doc.md", heading_level=2, content="x")
        result = str(chunk)
        assert result == "## My Section (doc.md)"

    def test_chunk_str_with_h1(self):
        chunk = Chunk(title="Title", file="a.md", heading_level=1, content="x")
        assert str(chunk) == "# Title (a.md)"

    def test_chunk_str_with_h3(self):
        chunk = Chunk(title="Sub", file="b.md", heading_level=3, content="x")
        assert str(chunk) == "### Sub (b.md)"

    def test_chunk_str_with_zero_level(self):
        """Level 0 means no heading — used for pre-heading content."""
        chunk = Chunk(title="Intro", file="c.md", heading_level=0, content="x")
        # Level 0 produces empty marker prefix
        result = str(chunk)
        assert "Intro" in result
        assert "(c.md)" in result


# ---------------------------------------------------------------------------
# Heading-aware chunking
# ---------------------------------------------------------------------------


class TestHeadingChunking:
    """Test heading-aware chunking behavior."""

    def test_h1_h2_h3_boundaries(self, temp_docs_dir):
        """Headings at H1, H2, H3 create separate chunks."""
        loader = MarkdownLoader(str(temp_docs_dir))
        chunks = loader.load()

        # The test-doc.md has: H1, H2, ### (H3), H2
        doc_chunks = [c for c in chunks if c.file == "test-doc.md"]
        levels = [c.heading_level for c in doc_chunks]
        assert 1 in levels, "H1 chunk should exist"
        assert 2 in levels, "H2 chunk should exist"
        assert 3 in levels, "H3 chunk should exist"

    def test_heading_titles_preserved(self, temp_docs_dir):
        """Each chunk should carry the heading title it was split on."""
        loader = MarkdownLoader(str(temp_docs_dir))
        chunks = loader.load()
        doc_chunks = [c for c in chunks if c.file == "test-doc.md"]
        titles = [c.title for c in doc_chunks]
        assert "Main Title" in titles
        assert "Section One" in titles
        assert "Subsection A" in titles
        assert "Section Two" in titles

    def test_h4_not_split(self, tmp_path):
        """H4 and deeper headings should NOT create new chunks."""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "h4.md").write_text(
            "# Title\n\nContent\n\n#### Deep Heading\n\nDeeper content\n",
            encoding="utf-8",
        )
        loader = MarkdownLoader(str(docs))
        chunks = loader.load()
        # Only 1 chunk because #### is not in HEADING_RE
        assert len(chunks) == 1
        # The #### line should be part of the content, not a boundary
        assert "#### Deep Heading" in chunks[0].content


# ---------------------------------------------------------------------------
# Code fence handling
# ---------------------------------------------------------------------------


class TestCodeFences:
    """Test that headings inside code fences are ignored."""

    def test_code_fence_headings_not_treated_as_boundaries(self, temp_docs_dir):
        """Headings inside code fences must not create new chunks."""
        loader = MarkdownLoader(str(temp_docs_dir))
        chunks = loader.load()
        fence_chunks = [c for c in chunks if c.file == "code-fence.md"]

        # Should have: "Real Heading" chunk and "After Code" chunk
        # The # inside ``` should NOT create a chunk
        titles = [c.title for c in fence_chunks]
        assert "This is not a heading" not in titles
        assert "Also not a heading" not in titles
        assert "After Code" in titles

    def test_code_inside_content_preserved(self, temp_docs_dir):
        """Code fence content should be preserved inside the chunk it belongs to."""
        loader = MarkdownLoader(str(temp_docs_dir))
        chunks = loader.load()
        fence_chunks = [c for c in chunks if c.file == "code-fence.md"]

        # The chunk containing the code fence should include the code
        real_heading_chunk = next(c for c in fence_chunks if c.title == "Real Heading")
        assert "# This is not a heading" in real_heading_chunk.content


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestLoaderEdgeCases:
    """Test edge cases for the loader."""

    def test_empty_file(self, tmp_path):
        """Empty markdown files should produce no chunks."""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "empty.md").write_text("", encoding="utf-8")
        loader = MarkdownLoader(str(docs))
        chunks = loader.load()
        assert len(chunks) == 0

    def test_missing_directory(self, tmp_path):
        """Non-existent directory should return empty list."""
        loader = MarkdownLoader(str(tmp_path / "nonexistent"))
        chunks = loader.load()
        assert chunks == []

    def test_file_instead_of_directory(self, tmp_path):
        """If path is a file (not dir), should return empty list."""
        f = tmp_path / "notadir.md"
        f.write_text("hello", encoding="utf-8")
        loader = MarkdownLoader(str(f))
        chunks = loader.load()
        assert chunks == []

    def test_no_headings_in_file(self, tmp_path):
        """A file with no headings gets one chunk titled by filename."""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "noheadings.md").write_text(
            "Just some plain text.\nNo headings here.\n",
            encoding="utf-8",
        )
        loader = MarkdownLoader(str(docs))
        chunks = loader.load()
        assert len(chunks) == 1
        assert chunks[0].title == "noheadings"
        assert chunks[0].heading_level == 0

    def test_file_with_only_code(self, tmp_path):
        """A file with only code and no headings should produce one chunk."""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "codeonly.md").write_text(
            "```python\ndef hello():\n    print('hi')\n```\n",
            encoding="utf-8",
        )
        loader = MarkdownLoader(str(docs))
        chunks = loader.load()
        assert len(chunks) == 1
        assert "```" in chunks[0].content

    def test_empty_docs_directory(self, temp_empty_docs_dir):
        """Directory with no .md files should return empty list."""
        loader = MarkdownLoader(str(temp_empty_docs_dir))
        chunks = loader.load()
        assert chunks == []

    def test_files_processed_in_sorted_order(self, tmp_path):
        """Files should be processed in sorted order for determinism."""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "z-last.md").write_text("# Z Last\n\nContent z.\n", encoding="utf-8")
        (docs / "a-first.md").write_text("# A First\n\nContent a.\n", encoding="utf-8")
        loader = MarkdownLoader(str(docs))
        chunks = loader.load()
        assert chunks[0].file == "a-first.md"
        assert chunks[1].file == "z-last.md"
