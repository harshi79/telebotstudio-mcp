"""Tests for server module functions."""

from __future__ import annotations

import json

import pytest

from loader import Chunk
from server import (
    MAX_QUERY_LENGTH,
    ConfigurationError,
    _format_page_chunks,
    _format_results,
    _validate_name,
    _validate_query,
    _validate_top_k,
    build_engine,
)

# ---------------------------------------------------------------------------
# _validate_query
# ---------------------------------------------------------------------------


class TestValidateQuery:
    def test_valid_query(self):
        assert _validate_query("telebot send message") == "telebot send message"

    def test_strips_whitespace(self):
        assert _validate_query("  telebot  ") == "telebot"

    def test_rejects_empty(self):
        with pytest.raises(ValueError, match="must not be empty"):
            _validate_query("")

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValueError, match="must not be empty"):
            _validate_query("   ")

    def test_rejects_too_long(self):
        with pytest.raises(ValueError, match="maximum length"):
            _validate_query("x" * (MAX_QUERY_LENGTH + 1))

    def test_accepts_max_length(self):
        # Exactly MAX_QUERY_LENGTH should be fine
        result = _validate_query("x" * MAX_QUERY_LENGTH)
        assert len(result) == MAX_QUERY_LENGTH


# ---------------------------------------------------------------------------
# _validate_top_k
# ---------------------------------------------------------------------------


class TestValidateTopK:
    def test_valid_top_k(self):
        assert _validate_top_k(5) == 5

    def test_minimum_value(self):
        assert _validate_top_k(1) == 1

    def test_maximum_value(self):
        assert _validate_top_k(50) == 50

    def test_rejects_less_than_1(self):
        with pytest.raises(ValueError, match="at least 1"):
            _validate_top_k(0)

    def test_rejects_negative(self):
        with pytest.raises(ValueError, match="at least 1"):
            _validate_top_k(-1)

    def test_rejects_greater_than_50(self):
        with pytest.raises(ValueError, match="at most 50"):
            _validate_top_k(51)

    def test_rejects_non_int(self):
        with pytest.raises(ValueError, match="must be an integer"):
            _validate_top_k("5")  # type: ignore


# ---------------------------------------------------------------------------
# _validate_name
# ---------------------------------------------------------------------------


class TestValidateName:
    def test_valid_name(self):
        assert _validate_name("getting-started") == "getting-started"

    def test_valid_name_with_dot(self):
        assert _validate_name("api-reference.md") == "api-reference.md"

    def test_valid_name_with_underscore(self):
        assert _validate_name("my_page") == "my_page"

    def test_rejects_empty(self):
        with pytest.raises(ValueError, match="must not be empty"):
            _validate_name("")

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValueError, match="must not be empty"):
            _validate_name("   ")

    def test_path_traversal_dotdot(self):
        """Path traversal with .. should be rejected."""
        with pytest.raises(ValueError):
            _validate_name("../../../etc/passwd")

    def test_path_traversal_slash(self):
        """Slashes are stripped by the allowlist; remaining safe chars form the name."""
        # 'subdir/file' → safe chars only → 'subdirfile'
        result = _validate_name("subdir/file")
        assert result == "subdirfile"

    def test_path_traversal_backslash(self):
        """Backslashes are stripped by the allowlist; remaining safe chars form the name."""
        # 'subdir\\file' → safe chars only → 'subdirfile'
        result = _validate_name("subdir\\file")
        assert result == "subdirfile"

    def test_strips_unsafe_chars(self):
        """Unsafe characters should be stripped, leaving only safe ones."""
        result = _validate_name("my-page@#$%")
        assert result == "my-page"


# ---------------------------------------------------------------------------
# _format_results
# ---------------------------------------------------------------------------


class TestFormatResults:
    def test_empty_results(self):
        result = _format_results([])
        parsed = json.loads(result)
        assert parsed["results"] == []
        assert "No matching" in parsed["message"]

    def test_with_results(self):
        chunk = Chunk(title="Test", file="test.md", heading_level=1, content="Hello")
        result = _format_results([(chunk, 1.5)])
        parsed = json.loads(result)
        assert len(parsed["results"]) == 1
        assert parsed["results"][0]["score"] == 1.5
        assert parsed["results"][0]["source"] == "test.md"
        assert parsed["results"][0]["heading"] == "Test"

    def test_score_rounded(self):
        chunk = Chunk(title="T", file="f.md", heading_level=1, content="C")
        result = _format_results([(chunk, 1.23456)])
        parsed = json.loads(result)
        assert parsed["results"][0]["score"] == 1.235


class TestFormatPageChunks:
    def test_empty_chunks(self):
        result = _format_page_chunks([])
        parsed = json.loads(result)
        assert parsed["results"] == []
        assert "not found" in parsed["message"].lower()

    def test_with_chunks(self):
        chunks = [
            Chunk(title="Intro", file="doc.md", heading_level=1, content="Hello"),
            Chunk(title="Details", file="doc.md", heading_level=2, content="World"),
        ]
        result = _format_page_chunks(chunks)
        parsed = json.loads(result)
        assert parsed["page"] == "doc.md"
        assert len(parsed["sections"]) == 2
        assert "full_content" in parsed
        assert "Hello" in parsed["full_content"]
        assert "World" in parsed["full_content"]


# ---------------------------------------------------------------------------
# build_engine
# ---------------------------------------------------------------------------


class TestBuildEngine:
    def test_raises_configuration_error_for_missing_dir(self, tmp_path):
        with pytest.raises(ConfigurationError, match="not found"):
            build_engine(str(tmp_path / "nonexistent"))

    def test_raises_configuration_error_for_file_instead_of_dir(self, tmp_path):
        f = tmp_path / "notadir.md"
        f.write_text("hello", encoding="utf-8")
        with pytest.raises(ConfigurationError, match="not a directory"):
            build_engine(str(f))

    def test_raises_configuration_error_for_empty_dir(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        with pytest.raises(ConfigurationError, match="No documentation chunks"):
            build_engine(str(empty))

    def test_builds_engine_successfully(self, tmp_path):
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "test.md").write_text("# Test\n\nContent here.\n", encoding="utf-8")
        engine = build_engine(str(docs))
        assert engine is not None
        assert len(engine.chunks) > 0
