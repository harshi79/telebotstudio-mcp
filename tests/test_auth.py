"""Tests for auth validation functions."""

from __future__ import annotations

import pytest

from api.auth import (
    validate_api_key,
    validate_bot_id,
    validate_bot_token,
    validate_command_code,
    validate_command_name,
)
from api.errors import ValidationError

# ---------------------------------------------------------------------------
# validate_api_key
# ---------------------------------------------------------------------------


class TestValidateApiKey:
    def test_valid_api_key(self):
        result = validate_api_key("tbs_abc123xyz")
        assert result == "tbs_abc123xyz"

    def test_strips_whitespace(self):
        result = validate_api_key("  tbs_abc123xyz  ")
        assert result == "tbs_abc123xyz"

    def test_rejects_empty(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_api_key("")

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_api_key("   ")

    def test_rejects_too_short(self):
        with pytest.raises(ValidationError, match="too short"):
            validate_api_key("abc")

    def test_rejects_too_long(self):
        with pytest.raises(ValidationError, match="too long"):
            validate_api_key("x" * 513)


# ---------------------------------------------------------------------------
# validate_bot_id
# ---------------------------------------------------------------------------


class TestValidateBotId:
    def test_valid_numeric(self):
        result = validate_bot_id("12345678")
        assert result == "12345678"

    def test_strips_whitespace(self):
        result = validate_bot_id("  12345  ")
        assert result == "12345"

    def test_rejects_empty(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_bot_id("")

    def test_rejects_non_numeric(self):
        with pytest.raises(ValidationError, match="must be numeric"):
            validate_bot_id("abc123")

    def test_rejects_alphanumeric(self):
        with pytest.raises(ValidationError, match="must be numeric"):
            validate_bot_id("12abc34")


# ---------------------------------------------------------------------------
# validate_bot_token
# ---------------------------------------------------------------------------


class TestValidateBotToken:
    def test_valid_format(self):
        token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz1234567890"
        result = validate_bot_token(token)
        assert result == token

    def test_strips_whitespace(self):
        token = "  123456789:ABCdefGHIjklMNOpqrsTUVwxyz1234567890  "
        result = validate_bot_token(token)
        assert result == token.strip()

    def test_rejects_empty(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_bot_token("")

    def test_rejects_invalid_format_no_colon(self):
        with pytest.raises(ValidationError, match="Invalid bot token format"):
            validate_bot_token("123456789ABCdefGHI")

    def test_rejects_invalid_format_wrong_prefix(self):
        with pytest.raises(ValidationError, match="Invalid bot token format"):
            validate_bot_token("abc:ABCdefGHIjklMNOpqrsTUVwxyz1234567890")

    def test_rejects_secret_too_short(self):
        with pytest.raises(ValidationError, match="Invalid bot token format"):
            validate_bot_token("12345:short")


# ---------------------------------------------------------------------------
# validate_command_name
# ---------------------------------------------------------------------------


class TestValidateCommandName:
    def test_valid_name(self):
        result = validate_command_name("start")
        assert result == "start"

    def test_strips_whitespace(self):
        result = validate_command_name("  start  ")
        assert result == "start"

    def test_rejects_empty(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_command_name("")

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_command_name("   ")

    def test_rejects_too_long(self):
        with pytest.raises(ValidationError, match="too long"):
            validate_command_name("x" * 257)


# ---------------------------------------------------------------------------
# validate_command_code
# ---------------------------------------------------------------------------


class TestValidateCommandCode:
    def test_valid_code(self):
        code = 'bot.send_message(chat_id, "Hello")'
        result = validate_command_code(code)
        assert result == code

    def test_strips_whitespace(self):
        result = validate_command_code("  print('hi')  ")
        assert result == "print('hi')"

    def test_rejects_empty(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_command_code("")

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_command_code("   ")

    def test_rejects_too_long(self):
        with pytest.raises(ValidationError, match="too long"):
            validate_command_code("x" * 50001)
