"""
TeleBot Studio API MCP Tools.

Registers 18 new MCP tools on the FastMCP server instance:

Credential Tools (3):
  - tbs_set_api_key
  - tbs_set_bot_id
  - tbs_credential_status

Bot Management Tools (3):
  - tbs_create_bot
  - tbs_delete_bot        (preview-supported)
  - tbs_update_bot_token  (preview-supported)

Command Management Tools (5):
  - tbs_create_command
  - tbs_get_command
  - tbs_update_command    (preview-supported)
  - tbs_delete_command    (preview-supported)
  - tbs_list_commands

Bot Control Tools (3):
  - tbs_start_bot
  - tbs_stop_bot
  - tbs_restart_bot

Agent Tools (2):
  - tbs_deploy_bot
  - tbs_setup_commands

Batch Tools (2):
  - tbs_batch_create_commands
  - tbs_batch_delete_commands  (preview-supported)
"""

from __future__ import annotations

import json
import logging
from typing import Any

from fastmcp import FastMCP

from api.auth import validate_api_key, validate_bot_id
from api.bot_control import BotControlManager
from api.bots import BotManager
from api.client import TeleBotStudioClient
from api.commands import CommandManager
from api.errors import TeleBotStudioError
from api.models import CommandDef
from api.session import CredentialManager

from agent.executor import Executor
from agent.planner import Planner
from agent.preview import Preview
from agent.validator import Validator

logger = logging.getLogger("telebotstudio-mcp.tools")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def register_api_tools(mcp: FastMCP) -> None:
    """Register all TeleBot Studio API tools on the FastMCP instance."""

    # ===================================================================
    # Credential Tools
    # ===================================================================

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

    # ===================================================================
    # Bot Management Tools
    # ===================================================================

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

    # ===================================================================
    # Command Management Tools
    # ===================================================================

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

    # ===================================================================
    # Bot Control Tools
    # ===================================================================

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

    # ===================================================================
    # Agent Tools
    # ===================================================================

    @mcp.tool
    def tbs_deploy_bot(
        bot_token: str,
        commands_json: str,
        confirm: bool = False,
    ) -> str:
        """
        Complete bot deployment: create bot, add commands, and start it.

        This is an agent-level tool that orchestrates multiple API calls
        in sequence. The AI uses this to fulfill high-level requests like
        "build me a bot" or "deploy a premium system."

        The bot ID from creation is automatically used for subsequent steps.

        Args:
            bot_token: Telegram bot token from @BotFather.
            commands_json: JSON array of command definitions.
                           Format: [{"name": "start", "code": "Api.sendMessage(...)"}]
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, execution results if confirm=True.
        """
        # Parse commands
        try:
            cmds_data = json.loads(commands_json)
            commands = [
                CommandDef(name=c["name"], code=c["code"]) for c in cmds_data
            ]
        except (json.JSONDecodeError, KeyError) as e:
            return _error_response(
                "validation_error",
                f"Invalid commands_json format: {e}. "
                'Expected: [{{"name": "start", "code": "Api.sendMessage(...)"}}]',
            )

        # Plan
        plan = Planner.plan_deploy_bot(bot_token, commands)

        # Validate
        valid, errors = Validator.validate_plan(plan)
        if not valid:
            return _error_response(
                "validation_error",
                "Plan validation failed",
                errors=errors,
            )

        # Preview
        if not confirm:
            return Preview.generate(plan)

        # Execute
        result = Executor.execute_plan(plan)
        return json.dumps(result.to_dict(), indent=2)

    @mcp.tool
    def tbs_setup_commands(
        commands_json: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Bulk create commands on an existing bot.

        This is an agent-level tool for setting up multiple commands at once.

        Args:
            commands_json: JSON array of command definitions.
                           Format: [{"name": "start", "code": "Api.sendMessage(...)"}]
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, execution results if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        # Parse commands
        try:
            cmds_data = json.loads(commands_json)
            commands = [
                CommandDef(name=c["name"], code=c["code"]) for c in cmds_data
            ]
        except (json.JSONDecodeError, KeyError) as e:
            return _error_response(
                "validation_error",
                f"Invalid commands_json format: {e}. "
                'Expected: [{{"name": "start", "code": "Api.sendMessage(...)"}}]',
            )

        # Plan
        plan = Planner.plan_setup_commands(bid, commands)

        # Validate
        valid, errors = Validator.validate_plan(plan)
        if not valid:
            return _error_response(
                "validation_error",
                "Plan validation failed",
                errors=errors,
            )

        # Preview
        if not confirm:
            return Preview.generate(plan)

        # Execute
        result = Executor.execute_plan(plan)
        return json.dumps(result.to_dict(), indent=2)

    # ===================================================================
    # Batch Tools
    # ===================================================================

    @mcp.tool
    def tbs_batch_create_commands(
        commands_json: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Create multiple commands on a bot in sequence.

        Each command is created independently. If one fails, the rest
        continue. A summary with per-command results is returned.

        Args:
            commands_json: JSON array of command definitions.
                           Format: [{"name": "start", "code": "Api.sendMessage(...)"}]
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, batch results if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        # Parse commands
        try:
            cmds_data = json.loads(commands_json)
            commands = [
                CommandDef(name=c["name"], code=c["code"]) for c in cmds_data
            ]
        except (json.JSONDecodeError, KeyError) as e:
            return _error_response(
                "validation_error",
                f"Invalid commands_json format: {e}. "
                'Expected: [{{"name": "start", "code": "Api.sendMessage(...)"}}]',
            )

        # Plan
        plan = Planner.plan_batch_create_commands(bid, commands)

        # Validate
        valid, errors = Validator.validate_plan(plan)
        if not valid:
            return _error_response(
                "validation_error",
                "Plan validation failed",
                errors=errors,
            )

        # Preview
        if not confirm:
            return Preview.generate(plan)

        # Execute
        result = Executor.execute_plan(plan)
        return json.dumps(result.to_dict(), indent=2)

    @mcp.tool
    def tbs_batch_delete_commands(
        command_names_json: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Delete multiple commands from a bot in sequence.

        This is a destructive operation. Each command is deleted independently.
        If one fails, the rest continue. A summary is returned.

        Args:
            command_names_json: JSON array of command names to delete.
                                Format: ["start", "help", "settings"]
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, batch results if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        # Parse command names
        try:
            names = json.loads(command_names_json)
            if not isinstance(names, list):
                raise ValueError("Expected a JSON array of strings")
        except (json.JSONDecodeError, ValueError) as e:
            return _error_response(
                "validation_error",
                f"Invalid command_names_json: {e}. "
                'Expected: ["start", "help", "settings"]',
            )

        # Plan
        plan = Planner.plan_batch_delete_commands(bid, names)

        # Validate
        valid, errors = Validator.validate_plan(plan)
        if not valid:
            return _error_response(
                "validation_error",
                "Plan validation failed",
                errors=errors,
            )

        # Preview
        if not confirm:
            return Preview.generate(plan)

        # Execute
        result = Executor.execute_plan(plan)
        return json.dumps(result.to_dict(), indent=2)
