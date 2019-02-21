from typing import Generator
from unittest import mock

import pytest
from aiohttp.web_app import Application

from app.app import make_app
from tests.helpers import MockedFetcher


@pytest.fixture
async def app() -> Application:
    return make_app()


@pytest.fixture
def client(loop, aiohttp_client, app: Application):
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def mocked_habra_fetch(app: Application) -> Generator[MockedFetcher, None, None]:
    with mock.patch.object(app['habra_fetcher'], 'fetch') as mocked_fetch:
        yield MockedFetcher(mocked_fetch)
