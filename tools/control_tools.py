"""
TeleBot Studio Bot Control MCP Tools.

Registers 3 bot control tools on the FastMCP server instance:
  - tbs_start_bot
  - tbs_stop_bot
  - tbs_restart_bot
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from api.bot_control import BotControlManager
from api.client import TeleBotStudioClient
from api.errors import TeleBotStudioError
from tools.helpers import _error_response, _get_bot_id_or_error, _require_api_key, _success_response

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_control_tools(mcp: FastMCP) -> None:
    """Register all bot control MCP tools on the FastMCP instance."""

    @mcp.tool
    def tbs_start_bot(bot_id: str = "") -> str:
        """
        Start a TeleBot Studio bot (set webhook).

        Args:
            bot_id: Bot ID. Uses session bot_id if not provided.

        Returns:
            JSON with start result.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                msg = BotControlManager(client).start(bid)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_stop_bot(bot_id: str = "") -> str:
        """
        Stop a TeleBot Studio bot (remove webhook).

        Args:
            bot_id: Bot ID. Uses session bot_id if not provided.

        Returns:
            JSON with stop result.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                msg = BotControlManager(client).stop(bid)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_restart_bot(bot_id: str = "") -> str:
        """
        Restart a TeleBot Studio bot (stop + start).

        Args:
            bot_id: Bot ID. Uses session bot_id if not provided.

        Returns:
            JSON with restart result.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                msg = BotControlManager(client).restart(bid)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))
