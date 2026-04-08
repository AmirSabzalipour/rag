from typing import Iterator
from xml.etree.ElementTree import Element

import html5lib


def parse_html(content: str) -> Element:
    return html5lib.parse(content, treebuilder="etree")


def strip_maybe(text: str | None) -> str | None:
    if text is None:
        return None
    text = text.strip()
    if not text:
        return None
    return text


def get_html_inner_text(element: Element) -> str:
    return "".join(element.itertext())


def get_html_text(element: Element) -> str | None:
    return strip_maybe(element.text)


def get_html_tail(element: Element) -> str | None:
    return strip_maybe(element.tail)


def get_html_tag(element: Element) -> str:
    # Example of a tag with namespace: {http://www.w3.org/1999/xhtml}h1
    return (
        element.tag.lower().strip().split("}")[-1]
    )  # Handle namespaces if present


def get_html_attr(element: Element, attr_name: str) -> str | None:
    return element.get(attr_name)


def iterate_html_children(element: Element) -> Iterator[Element]:
    return iter(element)


def list_html_children(element: Element) -> list[Element]:
    return list(element)


def list_html_selector(element: Element, selector: str) -> list[Element]:
    # this does not seem to select <main>
    return list(element.findall(selector))
