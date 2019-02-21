import re

import pytest
from aiohttp import test_utils

from app.helpers import add_symbols
from tests.helpers import MockedFetcher


@pytest.mark.parametrize('path', [
    '/hello', '/pupupupushka', '/ru/vasyan/100500/netu', '/', '',
])
async def test_called_with_path(client: test_utils.TestClient,
                                mocked_habra_fetch: MockedFetcher, path: str):
    mocked_habra_fetch.add_return_values({}, b'')
    response = await client.get(path)
    assert response.status == 200
    mocked_habra_fetch.check_call_with(path.replace('/', '', 1))


@pytest.mark.parametrize('habra_body,expected_text', [
    (b'vasya', 'vasya'),
    # replace src habr.com => 0.0.0.0:8080
    (b"<a src='https://habr.com/aaaaaaaa'> </a>", '<a src="http://0.0.0.0:8080/aaaaaaaa"></a>'),
    # div is changed
    (b'<div>bugaga I am Vasya</div>', '<div> bugaga™ I am Vasya</div>'),
    # script not changed
    (b'<script>const aaaaaa=100500</script>', '<script> const aaaaaa=100500</script>'),
])
async def test_correct_texts(
        client: test_utils.TestClient,
        mocked_habra_fetch: MockedFetcher,
        habra_body: bytes,
        expected_text: str):
    mocked_habra_fetch.add_return_values({'Content-Type': 'text/html'}, habra_body)
    response = await client.get('/')
    assert response.status == 200

    response_text = await response.text()
    assert response_text.replace('\n', '') == expected_text


@pytest.mark.parametrize('text,expected_text,add_symbol,searcher', [
    ('I am vasyok', 'I am vasyok@@@\n', '@@@', re.compile(r'(\w{6})')),
    ('I am vasyok I am the best of the best', 'I am™ vasyok I am™ the best of™ the best\n',
     '™', re.compile(r'\b\w{2}\b')),
])
async def test_words_add_symbols(text: str, add_symbol: str, expected_text: str, searcher):
    assert add_symbols(text, add_symbol, searcher=searcher) == expected_text
