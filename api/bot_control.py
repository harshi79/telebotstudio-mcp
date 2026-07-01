"""
Bot Control API Wrapper.

High-level methods for starting, stopping, and restarting bots
via the TeleBot Studio REST API v2.
"""

from __future__ import annotations

import logging

from api.auth import validate_bot_id
from api.client import TeleBotStudioClient

logger = logging.getLogger("telebotstudio-mcp.api.bot_control")


class BotControlManager:
    """Bot lifecycle operations (start, stop, restart)."""

    def __init__(self, client: TeleBotStudioClient):
        self._client = client

    def start(self, bot_id: str) -> str:
        """
        Start a bot by setting its webhook.

        Endpoint: POST /v2/bots/{botid}/start
        """
        bot_id = validate_bot_id(bot_id)

        response = self._client.post(f"/bots/{bot_id}/start")

        if response.ok:
            logger.info("Started bot: %s", bot_id)
            return str(response.result)

        raise ValueError(f"Failed to start bot: {response.result}")

    def stop(self, bot_id: str) -> str:
        """
        Stop a bot by removing its webhook.

        Endpoint: POST /v2/bots/{botid}/stop
        """
        bot_id = validate_bot_id(bot_id)

        response = self._client.post(f"/bots/{bot_id}/stop")

        if response.ok:
            logger.info("Stopped bot: %s", bot_id)
            return str(response.result)

        raise ValueError(f"Failed to stop bot: {response.result}")

    def restart(self, bot_id: str) -> str:
        """
        Stop and start a bot in one operation.

        Endpoint: POST /v2/bots/{botid}/restart
        """
        bot_id = validate_bot_id(bot_id)

        response = self._client.post(f"/bots/{bot_id}/restart")

        if response.ok:
            logger.info("Restarted bot: %s", bot_id)
            return str(response.result)

        raise ValueError(f"Failed to restart bot: {response.result}")
