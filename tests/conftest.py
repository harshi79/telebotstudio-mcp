"""Shared fixtures for the TeleBot Studio MCP test suite."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure the project root is on sys.path so we can import modules directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Sample Chunks
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_chunks():
    """Return a list of sample Chunk objects for search tests."""
    from loader import Chunk

    return [
        Chunk(
            title="Getting Started",
            file="getting-started.md",
            heading_level=1,
            content="Install the library with pip install telebot. Import using import telebot.",
        ),
        Chunk(
            title="API Reference",
            file="api-reference.md",
            heading_level=2,
            content=(
                "The API endpoint for sending messages. "
                "Parameter: chat_id. Return value: Message object."
            ),
        ),
        Chunk(
            title="Error Handling",
            file="errors.md",
            heading_level=2,
            content=(
                "Common error codes and exception handling. "
                "Debug traceback for troubleshooting."
            ),
        ),
        Chunk(
            title="Code Example",
            file="examples.md",
            heading_level=2,
            content=(
                "Here is a code example:\n"
                "```python\n"
                "bot = telebot.TeleBot('TOKEN')\n"
                "bot.send_message(chat_id, 'Hello')\n"
                "```"
            ),
        ),
        Chunk(
            title="Library Installation",
            file="installation.md",
            heading_level=1,
            content="To install the library, run pip install telebot. Setup your virtualenv first.",
        ),
    ]


@pytest.fixture
def sample_md_content():
    """Return a multi-section markdown string for loader tests."""
    return """# Main Title

This is the introduction.

## Section One

Content of section one.

### Subsection A

Details about subsection A.

## Section Two

Content of section two.
"""


@pytest.fixture
def sample_md_with_code_fences():
    """Return markdown with headings inside code fences (should be ignored)."""
    return """# Real Heading

Some intro text.

```
# This is not a heading
## Also not a heading
```

## After Code

Text after code fence.
"""


@pytest.fixture
def sample_md_code_only():
    """Return markdown with only code and no headings."""
    return """```python
def hello():
    print("Hello, World!")
```
"""


@pytest.fixture
def sample_md_empty():
    """Return an empty markdown string."""
    return ""


@pytest.fixture
def temp_docs_dir(tmp_path, sample_md_content, sample_md_with_code_fences):
    """Create a temporary docs directory with sample markdown files."""
    docs = tmp_path / "docs"
    docs.mkdir()

    (docs / "test-doc.md").write_text(sample_md_content, encoding="utf-8")
    (docs / "code-fence.md").write_text(sample_md_with_code_fences, encoding="utf-8")
    (docs / "simple.md").write_text("# Simple\n\nJust a simple page.\n", encoding="utf-8")

    return docs


@pytest.fixture
def temp_empty_docs_dir(tmp_path):
    """Create a temporary docs directory with no .md files."""
    docs = tmp_path / "empty_docs"
    docs.mkdir()
    return docs


@pytest.fixture
def fresh_credential_manager():
    """Reset CredentialManager state before and after each test."""
    from api.session import CredentialManager

    CredentialManager.cleanup_all_sessions()
    CredentialManager.set_session(None)
    yield CredentialManager
    CredentialManager.cleanup_all_sessions()
    CredentialManager.set_session(None)
