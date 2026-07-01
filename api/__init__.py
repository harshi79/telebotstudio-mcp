"""
TeleBot Studio API Client Layer.

Provides a typed, validated, retry-capable HTTP client for the
TeleBot Studio REST API v2 with session-scoped credential management.
"""

from api.client import TeleBotStudioClient
from api.errors import (
    AuthenticationError,
    ConnectionError,  # DEPRECATED: backward-compatible alias, shadows builtin
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
    TbsConnectionError,
    TeleBotStudioError,
    ValidationError,
)
from api.models import (
    ApiResponse,
    BotInfo,
    CommandInfo,
)
from api.session import CredentialManager

__all__ = [
    "ApiResponse",
    "AuthenticationError",
    "BotInfo",
    "CommandInfo",
    "ConnectionError",
    "CredentialManager",
    "RateLimitError",
    "ResourceNotFoundError",
    "ServerError",
    "TbsConnectionError",
    "TeleBotStudioClient",
    "TeleBotStudioError",
    "ValidationError",
]
