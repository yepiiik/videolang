from unittest.mock import patch
import pytest
from fastapi import HTTPException

from dependencies.auth import verify_api_key


class TestAuthDependency:
    def test_missing_api_key_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(api_key=None)

        assert exc_info.value.status_code == 401
        assert "Missing X-API-Key" in exc_info.value.detail

    def test_empty_string_api_key_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(api_key="")

        assert exc_info.value.status_code == 401

    def test_valid_api_key_increments_usage_and_returns_key(self):
        with patch("dependencies.auth.usage_tracker.increment_usage") as mock_increment:
            key = "valid-test-key-12345"
            result = verify_api_key(api_key=key)

            assert result == key
            mock_increment.assert_called_once_with(key)

    def test_rate_limit_exceeded_propagates_429(self):
        with patch(
            "dependencies.auth.usage_tracker.increment_usage",
            side_effect=HTTPException(status_code=429, detail="API rate limit exceeded"),
        ):
            with pytest.raises(HTTPException) as exc_info:
                verify_api_key(api_key="rate-limited-key")

            assert exc_info.value.status_code == 429
            assert "rate limit" in exc_info.value.detail.lower()
