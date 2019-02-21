import asyncio
import logging

import click

from app import app, clients

log = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
def runserver():
    app.runserver()


@cli.add_command
@click.command()
def runclient():
    async def fetch():
        fetcher = clients.Fetcher('https://habr.com/')
        try:
            headers, text = await fetcher.fetch('ru/post/89456/')
            log.info('Headers %s', headers)
            log.info('Response body %s', text)
            log.info('type %s', type(text))
        finally:
            await fetcher.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()
