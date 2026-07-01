"""
Bot Management API Wrapper.

High-level methods for creating, deleting, and updating bots
via the TeleBot Studio REST API v2.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from api.auth import validate_bot_id, validate_bot_token
from api.errors import ServerError, ValidationError
from api.models import BotInfo

if TYPE_CHECKING:
    from api.client import TeleBotStudioClient

logger = logging.getLogger("telebotstudio-mcp.api.bots")


class BotManager:
    """High-level bot management operations."""

    def __init__(self, client: TeleBotStudioClient):
        self._client = client

    def create(self, bot_token: str) -> BotInfo:
        """
        Create a new bot with a Telegram bot token.

        Endpoint: POST /v2/create-bot
        """
        bot_token = validate_bot_token(bot_token)

        response = self._client.post("/create-bot", json={"bot_token": bot_token})

        if response.ok and isinstance(response.result, dict):
            data = response.result
            bot_info = BotInfo(
                botid=str(data.get("botid", "")),
                bot_name=data.get("bot_name", ""),
                bot_username=data.get("bot_username", ""),
            )
            logger.info("Created bot: %s (%s)", bot_info.bot_name, bot_info.botid)
            return bot_info

        # If ok but result is a string, something unexpected happened
        raise ValidationError(f"Unexpected response format: {response.result}")

    def delete(self, bot_id: str) -> str:
        """
        Soft-delete a bot (marks as deleted, preserves data).

        Endpoint: DELETE /v2/bots/{botid}
        """
        bot_id = validate_bot_id(bot_id)

        response = self._client.delete(f"/bots/{bot_id}")

        if response.ok:
            logger.info("Deleted bot: %s", bot_id)
            return str(response.result)

        raise ServerError(f"Failed to delete bot: {response.result}")

    def update_token(self, bot_id: str, new_token: str) -> str:
        """
        Update the Telegram bot token for an existing bot.
        The bot is automatically started after the token is updated.

        Endpoint: POST /v2/bots/{botid}/update-bot-token
        """
        bot_id = validate_bot_id(bot_id)
        new_token = validate_bot_token(new_token)

        response = self._client.post(
            f"/bots/{bot_id}/update-bot-token",
            json={"token": new_token},
        )

        if response.ok:
            logger.info("Updated token for bot: %s", bot_id)
            return str(response.result)

        raise ServerError(f"Failed to update bot token: {response.result}")
