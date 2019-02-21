import re

from aiohttp import web

from app import settings
from app.helpers import add_symbols


async def habra_handler(request):
    path = request.match_info['path']

    habra_headers, habra_body = await request.app['habra_fetcher'].fetch(path)
    response_headers = {header: habra_headers[header] for header in settings.BASE_PROXY_HEADERS
                        if header in habra_headers}

    if not is_html_response(habra_headers):
        return web.Response(body=habra_body, headers=response_headers)

    # change buttons to our work
    habra_text = habra_body.decode('utf8')
    habra_text = habra_text.replace(
        'https://habr.com/',
        f'http://{settings.APP_HOST}:{settings.APP_PORT}/',
    )
    habra_text = add_symbols(habra_text, symbol='™', searcher=re.compile(r'\b\w{6}\b'))
    return web.Response(text=habra_text, headers=response_headers)


def is_html_response(headers):
    return 'text/html' in headers.get('Content-Type', '')
