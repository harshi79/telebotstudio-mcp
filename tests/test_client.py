"""Tests for TeleBotStudioClient (MOCKED — no real HTTP calls)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import httpx
import pytest

from api.client import TeleBotStudioClient
from api.errors import (
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
    TbsConnectionError,
    TeleBotStudioError,
    ValidationError,
)

# ---------------------------------------------------------------------------
# Helper to create mock httpx.Response
# ---------------------------------------------------------------------------


def make_mock_response(
    status_code: int = 200,
    body: dict | None = None,
    headers: dict | None = None,
) -> MagicMock:
    """Create a mock httpx.Response with the given status, body, and headers."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.headers = httpx.Headers(headers or {})
    if body is not None:
        resp.json.return_value = body
        resp.text = json.dumps(body)
    else:
        resp.json.side_effect = Exception("No JSON")
        resp.text = "non-json response"
    return resp


# ---------------------------------------------------------------------------
# _parse_response
# ---------------------------------------------------------------------------


class TestParseResponse:
    def setup_method(self):
        self.client = TeleBotStudioClient(api_key="tbs_test_key_123")

    def test_result_key(self):
        resp = make_mock_response(200, {"ok": True, "result": "success"})
        api_resp = self.client._parse_response(resp)
        assert api_resp.ok is True
        assert api_resp.result == "success"

    def test_commands_key(self):
        resp = make_mock_response(200, {"ok": True, "commands": [{"command": "start"}]})
        api_resp = self.client._parse_response(resp)
        assert api_resp.result == [{"command": "start"}]

    def test_command_key(self):
        resp = make_mock_response(200, {"ok": True, "command": {"command": "start"}})
        api_resp = self.client._parse_response(resp)
        assert api_resp.result == {"command": "start"}

    def test_no_recognized_key_ok_body(self):
        resp = make_mock_response(200, {"ok": True, "data": "value"})
        api_resp = self.client._parse_response(resp)
        assert api_resp.ok is True
        assert api_resp.result == {"ok": True, "data": "value"}

    def test_rate_limit_headers(self):
        resp = make_mock_response(
            200,
            {"ok": True, "result": "ok"},
            headers={"X-RateLimit-Remaining": "45", "X-RateLimit-Reset": "1700000000"},
        )
        api_resp = self.client._parse_response(resp)
        assert api_resp.rate_limit_remaining == 45
        assert api_resp.rate_limit_reset == 1700000000

    def test_non_json_response(self):
        resp = make_mock_response(200)
        api_resp = self.client._parse_response(resp)
        assert api_resp.ok is False


# ---------------------------------------------------------------------------
# _raise_for_status
# ---------------------------------------------------------------------------


class TestRaiseForStatus:
    def setup_method(self):
        self.client = TeleBotStudioClient(api_key="tbs_test_key_123")

    def test_200_no_exception(self):
        resp = make_mock_response(200, {"ok": True, "result": "ok"})
        api_resp = self.client._parse_response(resp)
        # Should not raise
        self.client._raise_for_status(resp, api_resp)

    def test_401_raises_authentication_error(self):
        resp = make_mock_response(401, {"ok": False, "result": "Unauthorized"})
        api_resp = self.client._parse_response(resp)
        with pytest.raises(AuthenticationError):
            self.client._raise_for_status(resp, api_resp)

    def test_404_raises_resource_not_found(self):
        resp = make_mock_response(404, {"ok": False, "result": "Not found"})
        api_resp = self.client._parse_response(resp)
        with pytest.raises(ResourceNotFoundError):
            self.client._raise_for_status(resp, api_resp)

    def test_400_raises_validation_error(self):
        resp = make_mock_response(400, {"ok": False, "result": "Bad request"})
        api_resp = self.client._parse_response(resp)
        with pytest.raises(ValidationError):
            self.client._raise_for_status(resp, api_resp)

    def test_429_raises_rate_limit_error(self):
        resp = make_mock_response(
            429,
            {"ok": False, "result": "Rate limited"},
            headers={"X-RateLimit-Reset": "1700000000"},
        )
        api_resp = self.client._parse_response(resp)
        with pytest.raises(RateLimitError) as exc_info:
            self.client._raise_for_status(resp, api_resp)
        assert exc_info.value.retry_after == 1700000000

    def test_500_raises_server_error(self):
        resp = make_mock_response(500, {"ok": False, "result": "Internal error"})
        api_resp = self.client._parse_response(resp)
        with pytest.raises(ServerError):
            self.client._raise_for_status(resp, api_resp)

    def test_418_raises_telebot_studio_error(self):
        resp = make_mock_response(418, {"ok": False, "result": "I'm a teapot"})
        api_resp = self.client._parse_response(resp)
        with pytest.raises(TeleBotStudioError):
            self.client._raise_for_status(resp, api_resp)


# ---------------------------------------------------------------------------
# Retry logic
# ---------------------------------------------------------------------------


class TestRetryLogic:
    @patch("api.client.TeleBotStudioClient._sleep")
    def test_retries_on_5xx_and_succeeds(self, mock_sleep):
        """Should retry on 5xx and succeed on the second attempt."""
        client = TeleBotStudioClient(api_key="tbs_test_key_123")

        resp_500 = make_mock_response(500, {"ok": False, "result": "Server error"})
        resp_200 = make_mock_response(200, {"ok": True, "result": "success"})

        with patch.object(client, "_open"):
            client._http = MagicMock()
            client._http.request.side_effect = [resp_500, resp_200]

            result = client.request("GET", "/test")
            assert result.ok is True
            assert mock_sleep.call_count == 1

    @patch("api.client.TeleBotStudioClient._sleep")
    def test_retries_exhausted_raises_server_error(self, mock_sleep):
        """After MAX_RETRIES, a 5xx should raise ServerError."""
        client = TeleBotStudioClient(api_key="tbs_test_key_123")

        resp_500 = make_mock_response(500, {"ok": False, "result": "Server error"})

        with patch.object(client, "_open"):
            client._http = MagicMock()
            client._http.request.return_value = resp_500

            with pytest.raises(ServerError):
                client.request("GET", "/test")

    def test_does_not_retry_on_4xx(self):
        """4xx errors should NOT be retried."""
        client = TeleBotStudioClient(api_key="tbs_test_key_123")

        resp_400 = make_mock_response(400, {"ok": False, "result": "Bad request"})

        with patch.object(client, "_open"):
            client._http = MagicMock()
            client._http.request.return_value = resp_400

            with pytest.raises(ValidationError):
                client.request("GET", "/test")
            # Should have been called only once (no retries)
            assert client._http.request.call_count == 1


# ---------------------------------------------------------------------------
# Auth headers
# ---------------------------------------------------------------------------


class TestAuthHeaders:
    def test_contains_bearer_token(self):
        client = TeleBotStudioClient(api_key="tbs_my_secret_key")
        headers = client._auth_headers()
        assert headers["Authorization"] == "Bearer tbs_my_secret_key"
        assert headers["Content-Type"] == "application/json"


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------


class TestContextManager:
    def test_context_manager_opens_and_closes(self):
        client = TeleBotStudioClient(api_key="tbs_test_key_123")
        with patch("api.client.httpx.Client") as MockHttp:
            mock_http_instance = MagicMock()
            MockHttp.return_value = mock_http_instance

            with client:
                assert client._http is not None

            mock_http_instance.close.assert_called_once()

    def test_close_idempotent(self):
        client = TeleBotStudioClient(api_key="tbs_test_key_123")
        # Close without opening should not raise
        client.close()
        client.close()


# ---------------------------------------------------------------------------
# Connection errors
# ---------------------------------------------------------------------------


class TestConnectionErrors:
    def test_connect_error_raises_tbs_connection_error(self):
        client = TeleBotStudioClient(api_key="tbs_test_key_123")

        with patch.object(client, "_open"):
            client._http = MagicMock()
            client._http.request.side_effect = httpx.ConnectError("Connection refused")

            with pytest.raises(TbsConnectionError, match="Cannot connect"):
                client.request("GET", "/test")
