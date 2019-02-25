import asyncio
import logging
import ssl
from typing import Tuple

import aiohttp
import multidict
from furl import furl

from app import settings

log = logging.getLogger(__name__)


class Fetcher:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(settings.MAX_CONNECTIONS_BY_FETCHER)
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True))
        self.request_params = {
            'ssl': ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH),
            'timeout': settings.CONNECTION_TIMOUT,
        }
        log.info('Create fetcher base_url=%s base_request_params=%s', base_url, self.request_params)

    async def fetch(self, path: str) -> Tuple[int, multidict.CIMultiDictProxy, bytes]:
        url = furl(self.base_url).add(path=path).url

        log.info('Fetcher fetch from url=%s', url)
        async with self.semaphore:
            async with self.session.get(url, **self.request_params) as response:  # type: ignore
                return response.status, response.headers, await response.read()

    async def close(self) -> None:
        await self.session.close()
