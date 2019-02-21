from aiohttp import web

from app import views
from app.clients import Fetcher


def runserver() -> None:
    web.run_app(make_app())


def make_app() -> web.Application:
    app = web.Application()

    app.add_routes([
        web.get(r'/{path:.*}', views.habra_handler),
    ])

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


async def on_startup(app: web.Application):
    app['habra_fetcher'] = Fetcher('https://habr.com/')


async def on_cleanup(app: web.Application):
    await app['habra_fetcher'].close()
