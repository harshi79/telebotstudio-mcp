"""Tests for ConnectionPool integration and idle/LRU eviction."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agent.executor import Executor
from agent.planner import Planner
from api.client import ConnectionPool, TeleBotStudioClient
from api.models import ApiResponse, CommandDef


class TestPoolIntegration:
    """Verify ConnectionPool serves its production purpose."""

    def teardown_method(self) -> None:
        TeleBotStudioClient.close_pool()

    def test_from_pool_reuses_same_api_key(self) -> None:
        """Same API key should retrieve the same pooled instance."""
        client1 = TeleBotStudioClient.from_pool(api_key="test_key_123")
        client2 = TeleBotStudioClient.from_pool(api_key="test_key_123")
        assert client1 is client2

    def test_from_pool_isolates_different_api_keys(self) -> None:
        """Different API keys should get separate instances."""
        client_a = TeleBotStudioClient.from_pool(api_key="key_a")
        client_b = TeleBotStudioClient.from_pool(api_key="key_b")
        assert client_a is not client_b

    def test_pool_keeps_client_alive_after_use(self) -> None:
        """Pooled clients should remain alive after ordinary usage."""
        client = TeleBotStudioClient.from_pool(api_key="alive_key")
        with patch("api.client.httpx.Client") as MockHttp:
            mock_http = MagicMock()
            MockHttp.return_value = mock_http
            with client:
                assert client._http is not None
        reused = TeleBotStudioClient.from_pool(api_key="alive_key")
        assert reused is client

    def test_pool_shutdown_closes_owned_clients(self) -> None:
        """close_pool() should close clients tracked by the pool."""
        TeleBotStudioClient.from_pool(api_key="shutdown_key")
        TeleBotStudioClient.close_pool()
        stats = TeleBotStudioClient.pool_stats()
        assert stats["active_clients"] == 0

    def test_direct_construction_still_works(self) -> None:
        """Direct TeleBotStudioClient creation must remain functional."""
        direct = TeleBotStudioClient(api_key="direct_key")
        assert direct._api_key == "direct_key"

    def test_executor_uses_pool(self, fresh_credential_manager) -> None:
        """Agent executor's execution path must reach from_pool() without network calls."""
        fresh_credential_manager.set_api_key("executor_pool_test")
        fresh_credential_manager.set_bot_id("12345")

        plan = Planner.plan_setup_commands(
            bot_id="12345",
            commands=[CommandDef(name="test", code="Api.sendMessage('ok')")],
        )

        mock_client = MagicMock(spec=TeleBotStudioClient)
        mock_client.post.return_value = ApiResponse(
            ok=True,
            result="Command created successfully",
            status_code=200,
        )

        with patch.object(
            TeleBotStudioClient, "from_pool", return_value=mock_client
        ) as mock_from_pool:
            result = Executor.execute_plan(plan)

        mock_from_pool.assert_called_once_with(api_key="executor_pool_test")
        assert result.total == 1
        assert result.succeeded == 1

    def test_pool_eviction_removes_idle_clients(self) -> None:
        """Pool should evict clients idle longer than idle_timeout."""
        pool = ConnectionPool(max_size=10, idle_timeout=60.0)
        with patch("api.client.time.monotonic", side_effect=[100.0, 100.0, 200.0, 200.0]):
            first = pool.get_client("idle_key")
            second = pool.get_client("idle_key")
            assert second is not first
        pool.close_all()

    def test_pool_lru_evicts_oldest_when_over_capacity(self) -> None:
        """Pool bounded at max_size should evict least-recently-used client."""
        pool = ConnectionPool(max_size=2, idle_timeout=0)
        c1 = pool.get_client("key_1")
        _c2 = pool.get_client("key_2")
        _c3 = pool.get_client("key_3")
        assert pool.active_client_count() == 2
        # Requesting key_1 again creates a fresh instance since it was evicted
        assert pool.get_client("key_1") is not c1
        pool.close_all()
