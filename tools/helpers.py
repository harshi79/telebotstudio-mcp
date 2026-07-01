"""
Shared helper functions for TeleBot Studio MCP tools.
"""

from __future__ import annotations

import json
from typing import Any

from api.auth import validate_bot_id
from api.session import CredentialManager


def _error_response(error_category: str, message: str, **extra: Any) -> str:
    """Build a structured error JSON response."""
    result: dict[str, Any] = {
        "ok": False,
        "error": error_category,
        "message": message,
    }
    result.update(extra)
    return json.dumps(result, indent=2)


def _success_response(data: Any, **extra: Any) -> str:
    """Build a structured success JSON response."""
    result: dict[str, Any] = {"ok": True, "result": data}
    result.update(extra)
    return json.dumps(result, indent=2)


def _require_api_key() -> str | None:
    """
    Retrieve the API key for the current session.

    Returns the API key string, or None if not set.
    """
    return CredentialManager.get_api_key()


def _get_bot_id_or_error(explicit_bot_id: str | None = None) -> tuple[str, str | None]:
    """
    Resolve bot_id from explicit param or session.
    Returns (bot_id, error_response_or_None).
    """
    if explicit_bot_id:
        try:
            return validate_bot_id(explicit_bot_id), None
        except Exception as e:
            return "", _error_response("validation_error", str(e))

    bid = CredentialManager.get_bot_id()
    if not bid:
        return "", _error_response(
            "credentials_required",
            "Bot ID not set. Use tbs_set_bot_id to specify which bot to operate on, "
            "or provide bot_id explicitly.",
        )
    return bid, None
