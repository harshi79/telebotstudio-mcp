"""
Authentication validation for TeleBot Studio API credentials.

Validates format and content before any HTTP request is made.
Never logs raw credentials.
"""

from __future__ import annotations

import re

from api.errors import ValidationError

# Telegram bot tokens look like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
# The numeric part is 1-15 digits, the secret part is 20-60 chars.
# Kept intentionally permissive — Telegram's format may evolve and
# BotFather test tokens can have non-standard lengths.
_BOT_TOKEN_RE = re.compile(r"^\d{1,15}:[A-Za-z0-9_-]{20,60}$")

# TeleBot Studio bot IDs are numeric strings
_BOT_ID_RE = re.compile(r"^\d+$")

# API keys are non-empty strings of reasonable length
_API_KEY_MIN_LENGTH = 8
_API_KEY_MAX_LENGTH = 512


def validate_api_key(api_key: str) -> str:
    """
    Validate and clean an API key.

    Returns the cleaned key on success.
    Raises ValidationError if the key is empty or too short/long.
    """
    if not api_key or not api_key.strip():
        raise ValidationError("API key must not be empty.")

    cleaned = api_key.strip()

    if len(cleaned) < _API_KEY_MIN_LENGTH:
        raise ValidationError(
            f"API key is too short (minimum {_API_KEY_MIN_LENGTH} characters)."
        )

    if len(cleaned) > _API_KEY_MAX_LENGTH:
        raise ValidationError(
            f"API key is too long (maximum {_API_KEY_MAX_LENGTH} characters)."
        )

    return cleaned


def validate_bot_id(bot_id: str) -> str:
    """
    Validate a TeleBot Studio bot ID.

    Returns the cleaned ID on success.
    Raises ValidationError if the ID is invalid.
    """
    if not bot_id or not bot_id.strip():
        raise ValidationError("Bot ID must not be empty.")

    cleaned = bot_id.strip()

    if not _BOT_ID_RE.match(cleaned):
        raise ValidationError(
            f"Bot ID must be numeric, got: '{cleaned}'. "
            "You can find your Bot ID in the TeleBot Studio dashboard."
        )

    return cleaned


def validate_bot_token(bot_token: str) -> str:
    """
    Validate a Telegram bot token format.

    Returns the cleaned token on success.
    Raises ValidationError if the token format is invalid.
    """
    if not bot_token or not bot_token.strip():
        raise ValidationError("Bot token must not be empty.")

    cleaned = bot_token.strip()

    if not _BOT_TOKEN_RE.match(cleaned):
        raise ValidationError(
            "Invalid bot token format. "
            "Expected format: '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'. "
            "Get your token from @BotFather on Telegram."
        )

    return cleaned


def validate_command_name(command_name: str) -> str:
    """
    Validate a command name.

    Returns the cleaned name on success.
    Raises ValidationError if the name is empty or too long.
    """
    if not command_name or not command_name.strip():
        raise ValidationError("Command name must not be empty.")

    cleaned = command_name.strip()

    if len(cleaned) > 256:
        raise ValidationError(
            f"Command name is too long (maximum 256 characters, got {len(cleaned)})."
        )

    return cleaned


def validate_command_code(code: str) -> str:
    """
    Validate command code.

    Returns the cleaned code on success.
    Raises ValidationError if the code is empty or too long.
    """
    if not code or not code.strip():
        raise ValidationError("Command code must not be empty.")

    if len(code) > 50000:
        raise ValidationError(
            f"Command code is too long (maximum 50000 characters, got {len(code)})."
        )

    return code.strip()
