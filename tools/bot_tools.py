"""
TeleBot Studio Bot Management MCP Tools.

Registers 3 bot management tools on the FastMCP server instance:
  - tbs_create_bot
  - tbs_delete_bot        (preview-supported)
  - tbs_update_bot_token  (preview-supported)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.preview import Preview
from api.bots import BotManager
from api.client import TeleBotStudioClient
from api.errors import TeleBotStudioError
from api.session import CredentialManager
from tools.helpers import _error_response, _get_bot_id_or_error, _require_api_key, _success_response

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_bot_tools(mcp: FastMCP) -> None:
    """Register all bot management MCP tools on the FastMCP instance."""

    @mcp.tool
    def tbs_create_bot(bot_token: str) -> str:
        """
        Create a new TeleBot Studio bot with a Telegram bot token.

        After creation, the bot ID is automatically set as the active
        bot for the current session.

        Get your bot token from @BotFather on Telegram.

        Args:
            bot_token: Telegram bot token (format: 123456789:ABCdef...).

        Returns:
            JSON with bot ID, name, and username on success.
        """
        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                info = BotManager(client).create(bot_token)

            # Auto-set the new bot as active
            CredentialManager.set_bot_id(info.botid)

            return _success_response(info.to_dict())
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_delete_bot(bot_id: str = "", confirm: bool = False) -> str:
        """
        Soft-delete a TeleBot Studio bot (marks as deleted, preserves data).

        This is a destructive operation. Set confirm=True to execute.
        When confirm=False (default), returns a preview of what will happen.

        Args:
            bot_id: Bot ID to delete. Uses session bot_id if not provided.
            confirm: Set to True to execute the deletion.

        Returns:
            Preview if confirm=False, deletion result if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        if not confirm:
            return Preview.generate_destructive_preview(
                action="delete_bot",
                description=f"Delete bot {bid} (soft delete — data preserved)",
                params={"bot_id": bid},
            )

        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                msg = BotManager(client).delete(bid)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_update_bot_token(
        bot_id: str = "",
        new_token: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Update the Telegram bot token for an existing bot.

        The bot is automatically restarted after the token update.
        This is a destructive operation. Set confirm=True to execute.

        Args:
            bot_id: Bot ID. Uses session bot_id if not provided.
            new_token: New Telegram bot token from @BotFather.
            confirm: Set to True to execute the update.

        Returns:
            Preview if confirm=False, update result if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        if not new_token:
            return _error_response(
                "validation_error", "new_token is required."
            )

        if not confirm:
            return Preview.generate_destructive_preview(
                action="update_bot_token",
                description=f"Update token for bot {bid} (bot will restart)",
                params={"bot_id": bid},
            )

        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                msg = BotManager(client).update_token(bid, new_token)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))
