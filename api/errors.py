"""
TeleBot Studio API Exception Hierarchy.

Every API error is mapped to a typed exception so MCP tools can
produce structured, actionable error responses.

NOTE: ``TbsConnectionError`` is used instead of ``ConnectionError``
to avoid shadowing the Python builtin.
"""

from __future__ import annotations


class TeleBotStudioError(Exception):
    """Base exception for all TeleBot Studio API errors."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    @property
    def error_category(self) -> str:
        return "api_error"


class AuthenticationError(TeleBotStudioError):
    """401 — Invalid, missing, or expired API key."""

    @property
    def error_category(self) -> str:
        return "authentication_error"


class ResourceNotFoundError(TeleBotStudioError):
    """404 — Bot or command not found, or not owned by the user."""

    @property
    def error_category(self) -> str:
        return "not_found_error"


class ValidationError(TeleBotStudioError):
    """400 — Invalid request parameters (bad token format, missing fields)."""

    @property
    def error_category(self) -> str:
        return "validation_error"


class RateLimitError(TeleBotStudioError):
    """429 — Rate limit exceeded."""

    def __init__(
        self,
        message: str,
        *,
        retry_after: int | None = None,
        status_code: int | None = None,
    ):
        super().__init__(message, status_code=status_code)
        self.retry_after = retry_after

    @property
    def error_category(self) -> str:
        return "rate_limit_error"


class ServerError(TeleBotStudioError):
    """5xx — Server-side error."""

    @property
    def error_category(self) -> str:
        return "server_error"


class TbsConnectionError(TeleBotStudioError):
    """Network-level failure (timeout, DNS, connection refused)."""

    @property
    def error_category(self) -> str:
        return "connection_error"


# Backward-compatible alias (DO NOT use in new code)
# Intentionally prefixed with "Tbs" to avoid shadowing Python's builtin ConnectionError.
# This alias exists solely for any external consumers; internal code uses TbsConnectionError.
ConnectionError = TbsConnectionError  # noqa: A001
