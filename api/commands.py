"""
Command Management API Wrapper.

High-level methods for creating, reading, updating, and deleting
bot commands via the TeleBot Studio REST API v2.

Uses the recommended /command/by-name endpoints (no Base64 encoding
required).
"""

from __future__ import annotations

import logging

from api.auth import validate_bot_id, validate_command_name, validate_command_code
from api.client import TeleBotStudioClient
from api.models import CommandInfo

logger = logging.getLogger("telebotstudio-mcp.api.commands")


class CommandManager:
    """High-level command management operations."""

    def __init__(self, client: TeleBotStudioClient):
        self._client = client

    def create(self, bot_id: str, command: str, code: str) -> str:
        """
        Create a new command for a bot.

        Endpoint: POST /v2/bots/{botid}/commands
        """
        bot_id = validate_bot_id(bot_id)
        command = validate_command_name(command)
        code = validate_command_code(code)

        response = self._client.post(
            f"/bots/{bot_id}/commands",
            json={"command": command, "code": code},
        )

        if response.ok:
            logger.info("Created command '%s' on bot %s", command, bot_id)
            return str(response.result)

        raise ValueError(f"Failed to create command: {response.result}")

    def get(self, bot_id: str, command_name: str) -> CommandInfo:
        """
        Get a command's details by name.

        Endpoint: POST /v2/bots/{botid}/command/by-name

        NOTE: The API documentation states GET, but the live API
        only accepts POST with a JSON body.  This was verified
        against the production API (returns 405 for GET).
        """
        bot_id = validate_bot_id(bot_id)
        command_name = validate_command_name(command_name)

        response = self._client.post(
            f"/bots/{bot_id}/command/by-name",
            json={"command_name": command_name},
        )

        if response.ok and isinstance(response.result, dict):
            data = response.result
            return CommandInfo(
                command=data.get("command", command_name),
                code=data.get("code", ""),
                is_pinned=data.get("is_pinned", False),
            )

        raise ValueError(f"Failed to get command: {response.result}")

    def update(self, bot_id: str, command_name: str, code: str) -> str:
        """
        Update an existing command's code.

        Endpoint: POST /v2/bots/{botid}/command/by-name/update
        """
        bot_id = validate_bot_id(bot_id)
        command_name = validate_command_name(command_name)
        code = validate_command_code(code)

        response = self._client.post(
            f"/bots/{bot_id}/command/by-name/update",
            json={"command_name": command_name, "code": code},
        )

        if response.ok:
            logger.info("Updated command '%s' on bot %s", command_name, bot_id)
            return str(response.result)

        raise ValueError(f"Failed to update command: {response.result}")

    def delete(self, bot_id: str, command_name: str) -> str:
        """
        Delete a command from a bot.

        Endpoint: POST /v2/bots/{botid}/command/by-name/delete
        """
        bot_id = validate_bot_id(bot_id)
        command_name = validate_command_name(command_name)

        response = self._client.post(
            f"/bots/{bot_id}/command/by-name/delete",
            json={"command_name": command_name},
        )

        if response.ok:
            logger.info("Deleted command '%s' on bot %s", command_name, bot_id)
            return str(response.result)

        raise ValueError(f"Failed to delete command: {response.result}")

    def list_all(self, bot_id: str) -> list[CommandInfo]:
        """
        List all commands for a bot.

        Endpoint: GET /v2/bots/{botid}/commands/list

        NOTE: The API documentation states GET /bots/{botid}/commands,
        but the live API only accepts POST on that path (for creating
        commands).  The actual list endpoint is /commands/list.
        This was verified against the production API.
        """
        bot_id = validate_bot_id(bot_id)

        response = self._client.get(f"/bots/{bot_id}/commands/list")

        if response.ok:
            # The API returns {"ok": true, "commands": [...]}
            # Our client parses the top-level body; commands are in the raw response
            # We need to handle both cases
            raw = response.result
            if isinstance(raw, dict) and "commands" in raw:
                commands_data = raw["commands"]
            elif isinstance(raw, list):
                commands_data = raw
            else:
                commands_data = []

            return [
                CommandInfo(
                    command=cmd.get("command", ""),
                    code=cmd.get("code", ""),
                    is_pinned=cmd.get("is_pinned", False),
                )
                for cmd in commands_data
            ]

        raise ValueError(f"Failed to list commands: {response.result}")
