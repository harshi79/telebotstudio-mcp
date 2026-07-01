"""
TeleBot Studio Credential MCP Tools.

Registers 3 credential-related tools on the FastMCP server instance:
  - tbs_set_api_key
  - tbs_set_bot_id
  - tbs_credential_status
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from api.auth import validate_api_key, validate_bot_id
from api.session import CredentialManager
from tools.helpers import _error_response, _success_response

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_credential_tools(mcp: FastMCP) -> None:
    """Register all credential-related MCP tools on the FastMCP instance."""

    @mcp.tool
    def tbs_set_api_key(api_key: str) -> str:
        """
        Set your TeleBot Studio API key for the current session.

        The API key is stored in memory only — never persisted to disk,
        never logged in cleartext. It is lost when the server restarts.

        You can find your API key at:
        telebotstudio.com → Account Settings → API

        Args:
            api_key: Your TeleBot Studio API key.

        Returns:
            Confirmation that the key was set (key is masked in response).
        """
        try:
            cleaned = validate_api_key(api_key)
        except Exception as e:
            return _error_response("validation_error", str(e))

        CredentialManager.set_api_key(cleaned)
        status = CredentialManager.status()
        return _success_response(
            "API key set for current session",
            api_key_preview=status["api_key_preview"],
        )

    @mcp.tool
    def tbs_set_bot_id(bot_id: str) -> str:
        """
        Set the active TeleBot Studio Bot ID for the current session.

        This bot ID will be used for all bot-scoped operations
        (commands, start, stop, restart) unless overridden explicitly.

        Args:
            bot_id: Your TeleBot Studio bot ID (numeric).

        Returns:
            Confirmation that the bot ID was set.
        """
        try:
            cleaned = validate_bot_id(bot_id)
        except Exception as e:
            return _error_response("validation_error", str(e))

        CredentialManager.set_bot_id(cleaned)
        return _success_response(
            f"Bot ID set to {cleaned} for current session",
        )

    @mcp.tool
    def tbs_credential_status() -> str:
        """
        Check the current session credential status.

        Returns whether the API key and Bot ID are set (key is masked).
        Use this to verify your credentials before performing API operations.

        Returns:
            JSON with api_key_set, api_key_preview, bot_id_set, bot_id.
        """
        return json.dumps(CredentialManager.status(), indent=2)
