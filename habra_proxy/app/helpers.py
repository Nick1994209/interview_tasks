import re

from bs4 import BeautifulSoup


def add_symbols(
        text: str,
        symbol: str,
        searcher: re.Pattern,  # type: ignore
        ignore_tags=frozenset(
            ['html', 'title', 'style', 'head', 'script', 'pre', 'code', 'meta', 'img']
        ),
) -> str:
    soup = BeautifulSoup(text, "html.parser")

    for tag in soup.findAll(text=True):
        if tag.parent.name in ignore_tags:
            continue

        edited_text = searcher.sub(lambda matched: matched.group(0) + symbol, tag.string)
        tag.replace_with(edited_text)
    return soup.prettify()
