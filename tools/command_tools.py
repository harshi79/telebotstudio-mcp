"""
TeleBot Studio Command Management MCP Tools.

Registers 5 command management tools on the FastMCP server instance:
  - tbs_create_command
  - tbs_get_command
  - tbs_update_command    (preview-supported)
  - tbs_delete_command    (preview-supported)
  - tbs_list_commands
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.preview import Preview
from api.client import TeleBotStudioClient
from api.commands import CommandManager
from api.errors import TeleBotStudioError
from tools.helpers import _error_response, _get_bot_id_or_error, _require_api_key, _success_response

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_command_tools(mcp: FastMCP) -> None:
    """Register all command management MCP tools on the FastMCP instance."""

    @mcp.tool
    def tbs_create_command(
        command: str,
        code: str,
        bot_id: str = "",
    ) -> str:
        """
        Create a new command on a TeleBot Studio bot.

        Args:
            command: Command name (e.g., "start" or "/start").
            code: TeleBot Studio code for the command
                  (e.g., "Api.sendMessage('Hello!')").
            bot_id: Bot ID. Uses session bot_id if not provided.

        Returns:
            JSON with creation result on success.
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
                msg = CommandManager(client).create(bid, command, code)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_get_command(command_name: str, bot_id: str = "") -> str:
        """
        Get details of a specific command by name.

        Args:
            command_name: The command name to look up.
            bot_id: Bot ID. Uses session bot_id if not provided.

        Returns:
            JSON with command details (name, code, is_pinned).
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
                info = CommandManager(client).get(bid, command_name)
            return _success_response(info.to_dict())
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_update_command(
        command_name: str,
        code: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Update an existing command's code.

        This is a destructive operation. Set confirm=True to execute.
        When confirm=False, returns a preview.

        Args:
            command_name: Name of the command to update.
            code: New code for the command.
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute the update.

        Returns:
            Preview if confirm=False, update result if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        if not confirm:
            return Preview.generate_destructive_preview(
                action="update_command",
                description=f"Update command '/{command_name}' on bot {bid}",
                params={"bot_id": bid, "command_name": command_name},
            )

        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                msg = CommandManager(client).update(bid, command_name, code)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_delete_command(
        command_name: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Delete a command from a TeleBot Studio bot.

        This is a destructive operation. Set confirm=True to execute.
        When confirm=False, returns a preview.

        Args:
            command_name: Name of the command to delete.
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute the deletion.

        Returns:
            Preview if confirm=False, deletion result if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        if not confirm:
            return Preview.generate_destructive_preview(
                action="delete_command",
                description=f"Delete command '/{command_name}' from bot {bid}",
                params={"bot_id": bid, "command_name": command_name},
            )

        api_key = _require_api_key()
        if not api_key:
            return _error_response(
                "credentials_required",
                "API key not set. Use tbs_set_api_key first.",
            )

        try:
            with TeleBotStudioClient(api_key=api_key) as client:
                msg = CommandManager(client).delete(bid, command_name)
            return _success_response(msg)
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))

    @mcp.tool
    def tbs_list_commands(bot_id: str = "") -> str:
        """
        List all commands for a TeleBot Studio bot.

        Args:
            bot_id: Bot ID. Uses session bot_id if not provided.

        Returns:
            JSON with list of commands (name, code, is_pinned).
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
                commands = CommandManager(client).list_all(bid)
            return _success_response(
                [c.to_dict() for c in commands],
                total=len(commands),
            )
        except TeleBotStudioError as e:
            return _error_response(e.error_category, e.message)
        except Exception as e:
            return _error_response("unexpected_error", str(e))
