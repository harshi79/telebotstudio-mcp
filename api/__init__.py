"""
TeleBot Studio API Client Layer.

Provides a typed, validated, retry-capable HTTP client for the
TeleBot Studio REST API v2 with session-scoped credential management.
"""

from api.errors import (
    TeleBotStudioError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    TbsConnectionError,
    ConnectionError,  # backward-compatible alias
)
from api.models import (
    ApiResponse,
    BotInfo,
    CommandInfo,
)
from api.session import CredentialManager
from api.client import TeleBotStudioClient

__all__ = [
    "TeleBotStudioError",
    "AuthenticationError",
    "ResourceNotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "TbsConnectionError",
    "ConnectionError",
    "ApiResponse",
    "BotInfo",
    "CommandInfo",
    "CredentialManager",
    "TeleBotStudioClient",
]
