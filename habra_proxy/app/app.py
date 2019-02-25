import re

from aiohttp import web

from app import settings, views
from app.clients import Fetcher


def runserver() -> None:
    web.run_app(make_app(), host=settings.APP_HOST, port=settings.APP_PORT)


def make_app() -> web.Application:
    app = web.Application()

    app.add_routes([
        web.get(r'/{path:.*}', views.habra_proxy_handler),
    ])

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


async def on_startup(app: web.Application):
    app['habra_fetcher'] = Fetcher('https://habr.com/')
    # regular expression is required for changing words and add ™
    app['habra_word_change_finder'] = re.compile(r'\b\w{6}\b')


async def on_cleanup(app: web.Application):
    await app['habra_fetcher'].close()
