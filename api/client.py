"""
Core HTTP client for the TeleBot Studio REST API v2.

Handles:
  - Bearer token authentication
  - Retry with exponential backoff (transient 5xx only)
  - Timeout management
  - Rate-limit header extraction
  - Error response → typed exception mapping
  - Connection lifecycle (always closed in finally)
"""

from __future__ import annotations

import contextlib
import logging
from typing import Any

import httpx

from api.errors import (
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
    TbsConnectionError,
    TeleBotStudioError,
    ValidationError,
)
from api.models import ApiResponse
from api.utils import async_sleep

logger = logging.getLogger("telebotstudio-mcp.client")

DEFAULT_BASE_URL = "https://api.telebotstudio.com/v2"
DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3
RETRY_BACKOFF = [1, 2, 4]  # seconds


class TeleBotStudioClient:
    """Low-level HTTP client for the TeleBot Studio REST API v2."""

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self._api_key = api_key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout
        self._http: httpx.Client | None = None

    # ---- Context Manager ----

    def __enter__(self) -> TeleBotStudioClient:
        self._open()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def _open(self) -> None:
        """Open the underlying httpx client."""
        if self._http is None:
            self._http = httpx.Client(
                base_url=self._base_url,
                timeout=self._timeout,
                headers=self._auth_headers(),
            )

    def close(self) -> None:
        """Close the underlying httpx client."""
        if self._http is not None:
            with contextlib.suppress(Exception):
                self._http.close()
            self._http = None

    # ---- Auth ----

    def _auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    # ---- Public Request Methods ----

    def get(self, path: str, *, params: dict | None = None) -> ApiResponse:
        """Send a GET request."""
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
    ) -> ApiResponse:
        """Send a POST request."""
        return self.request("POST", path, json=json, params=params)

    def delete(self, path: str) -> ApiResponse:
        """Send a DELETE request."""
        return self.request("DELETE", path)

    # ---- Core Request Logic ----

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
    ) -> ApiResponse:
        """
        Send an HTTP request with retry logic.

        Retries on:
          - 5xx responses (up to MAX_RETRIES with exponential backoff)
          - httpx.TimeoutException

        Does NOT retry on:
          - 4xx responses (client errors are final)
        """
        self._open()
        assert self._http is not None

        last_exception: Exception | None = None
        last_api_response: ApiResponse | None = None

        for attempt in range(MAX_RETRIES):
            try:
                response = self._http.request(
                    method,
                    path,
                    json=json,
                    params=params,
                )

                api_response = self._parse_response(response)
                last_api_response = api_response

                # Retry on server errors (5xx), but NOT on the last attempt
                if response.status_code >= 500 and attempt < MAX_RETRIES - 1:
                    backoff = RETRY_BACKOFF[attempt]
                    logger.warning(
                        "Server error %d on %s %s (attempt %d/%d), retrying in %ds",
                        response.status_code,
                        method,
                        path,
                        attempt + 1,
                        MAX_RETRIES,
                        backoff,
                    )
                    self._sleep(backoff)
                    continue

                # Map error status codes to exceptions (including final 5xx)
                self._raise_for_status(response, api_response)

                return api_response

            except httpx.TimeoutException as exc:
                last_exception = exc
                if attempt < MAX_RETRIES - 1:
                    backoff = RETRY_BACKOFF[attempt]
                    logger.warning(
                        "Timeout on %s %s (attempt %d/%d), retrying in %ds",
                        method,
                        path,
                        attempt + 1,
                        MAX_RETRIES,
                        backoff,
                    )
                    self._sleep(backoff)
                    continue

            except httpx.ConnectError as exc:
                raise TbsConnectionError(
                    f"Cannot connect to TeleBot Studio API at {self._base_url}. "
                    "Check your internet connection."
                ) from exc

            except TeleBotStudioError:
                raise  # Don't retry our own typed errors

            except httpx.HTTPError as exc:
                raise TbsConnectionError(
                    f"HTTP error communicating with TeleBot Studio API: {exc}"
                ) from exc

        # All retries exhausted
        if last_exception is not None:
            raise TbsConnectionError(
                f"Request to {method} {path} failed after {MAX_RETRIES} attempts: "
                f"{last_exception}"
            )

        # If we got here with a 5xx on the last attempt, raise ServerError
        if last_api_response is not None and last_api_response.status_code >= 500:
            raise ServerError(
                str(last_api_response.result) or f"HTTP {last_api_response.status_code}",
                status_code=last_api_response.status_code,
            )

        raise TbsConnectionError(
            f"Request to {method} {path} failed after all retries."
        )

    # ---- Sleep Helper ----

    @staticmethod
    def _sleep(seconds: float) -> None:
        """Delegate to the shared async-aware sleep utility."""
        async_sleep(seconds)

    # ---- Response Parsing ----

    def _parse_response(self, response: httpx.Response) -> ApiResponse:
        """Parse an httpx response into an ApiResponse."""
        rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
        rate_limit_reset = response.headers.get("X-RateLimit-Reset")

        try:
            body = response.json()
        except Exception:
            body = {"ok": False, "result": response.text}

        # Extract the primary result from the response body.
        # The TeleBot Studio API uses different keys depending on endpoint:
        #   - Most endpoints: {"ok": true, "result": "..."}
        #   - List commands:   {"ok": true, "commands": [...]}
        #   - Get command:     {"ok": true, "command": {...}}
        # We prioritize "result", then fall back to known alternatives.
        if "result" in body:
            result_data = body["result"]
        elif "commands" in body:
            result_data = body["commands"]
        elif "command" in body:
            result_data = body["command"]
        else:
            # For success responses with no recognized key, use the entire body
            result_data = body if body.get("ok") else body.get("result", str(body))

        return ApiResponse(
            ok=body.get("ok", False),
            result=result_data,
            status_code=response.status_code,
            rate_limit_remaining=(
                int(rate_limit_remaining) if rate_limit_remaining else None
            ),
            rate_limit_reset=(
                int(rate_limit_reset) if rate_limit_reset else None
            ),
        )

    # ---- Error Mapping ----

    @staticmethod
    def _raise_for_status(
        response: httpx.Response, api_response: ApiResponse
    ) -> None:
        """Map HTTP status codes to typed exceptions."""
        code = response.status_code

        if 200 <= code < 300:
            return  # Success, no exception

        error_msg = str(api_response.result) if api_response.result else f"HTTP {code}"

        if code == 401:
            raise AuthenticationError(error_msg, status_code=code)
        elif code == 404:
            raise ResourceNotFoundError(error_msg, status_code=code)
        elif code == 400:
            raise ValidationError(error_msg, status_code=code)
        elif code == 429:
            retry_after = api_response.rate_limit_reset
            raise RateLimitError(
                error_msg, retry_after=retry_after, status_code=code
            )
        elif code >= 500:
            raise ServerError(error_msg, status_code=code)
        else:
            raise TeleBotStudioError(error_msg, status_code=code)
