import re
from typing import Iterable

from bs4 import BeautifulSoup, element


def add_symbols(
    text: str,
    symbol: str,
    searcher: re.Pattern,  # type: ignore
    ignore_tags: Iterable = frozenset([
        'html', '[document]', 'title', 'style', 'head', 'script', 'noscript',
        'pre', 'code', 'meta', 'img'
    ]),
    ignore_tag_types: Iterable = (element.Doctype, element.Comment, element.Declaration),
) -> str:
    soup = BeautifulSoup(text, "html.parser")

    for tag in soup.findAll(text=True):
        if tag.parent.name in ignore_tags or type(tag) in ignore_tag_types:
            continue

        edited_text = searcher.sub(lambda matched: matched.group(0) + symbol, tag.string)
        tag.replace_with(edited_text)
    return soup.prettify()
