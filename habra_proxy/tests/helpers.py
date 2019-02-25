from dataclasses import dataclass
from typing import Dict
from unittest import mock


@dataclass
class MockedFetcher:
    mocked_fetch: mock.MagicMock

    def add_return_values(self, status_code: int, headers: Dict, body: bytes) -> None:
        async def coro():
            return status_code, headers, body
        self.mocked_fetch.return_value = coro()

    def check_call_with(self, path: str) -> None:
        self.mocked_fetch.assert_called_with(path)
