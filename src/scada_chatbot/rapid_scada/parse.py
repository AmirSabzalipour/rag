from typing import Tuple

from scada_chatbot.document.__types__ import (
    DocFigure,
    DocFragment,
    DocFragmentStyle,
    DocList,
    DocListItem,
    DocListing,
    DocParagraph,
    DocLocator,
    DocNode,
    DocSection,
    DocSectionNode,
    DocTable,
    DocTableCell,
    DocTableRow,
)
from scada_chatbot.document.locator import locate_element, make_root_locator
from scada_chatbot.parsing.html import (
    Element,
    get_html_attr,
    get_html_inner_text,
    get_html_tail,
    get_html_text,
    get_html_tag,
    iterate_html_children,
    list_html_children,
    list_html_selector,
    parse_html,
)


def locate_position(
    locator: DocLocator,
    index: int,
) -> DocLocator:
    return DocLocator(f"{locator}/{index}")


def to_plain_text_fragment(text: str) -> DocFragment:
    return {
        "type": "text",
        "style": "none",
        "content": text,
    }


def assertNoTail(element: Element, locator: DocLocator) -> None:
    tail = get_html_tail(element)
    if tail is not None:
        raise ValueError(
            f"Expected no tail text in element at {locator}, but found tail: '{tail}'"
        )


def assertNoText(element: Element, locator: DocLocator) -> None:
    text = get_html_text(element)
    if text is not None:
        raise ValueError(
            f"Expected no inner text in element at {locator}, but found text: '{text}'"
        )


def get_fragment_style(tag: str) -> DocFragmentStyle:
    if tag == "em":
        return "emph"
    elif tag == "strong":
        return "strong"
    elif tag == "code":
        return "code"
    elif tag == "pre":
        return "code"
    else:
        return "none"


def visit_fragment(element: Element) -> None | DocFragment:
    text = get_html_inner_text(element)
    if text is None:
        return None
    if get_html_tag(element) == "a":
        href = get_html_attr(element, "href")
        if href is None:
            raise ValueError(
                f"Expected <a> element to have 'href' attribute, but found none at {element}"
            )
        return {
            "type": "link",
            "content": text,
            "link": href,
        }
    else:
        return {
            "type": "text",
            "content": text,
            "style": get_fragment_style(get_html_tag(element)),
        }


def visit_fragment_container(element: Element) -> list[DocFragment]:
    fragments: list[DocFragment] = []
    text = get_html_text(element)
    if text:
        fragments.append(to_plain_text_fragment(text))
    for child in iterate_html_children(element):
        fragment = visit_fragment(child)
        if fragment is not None:
            fragments.append(fragment)
        tail = get_html_tail(child)
        if tail:
            fragments.append(to_plain_text_fragment(tail))
    tail = get_html_tail(element)
    if tail:
        fragments.append(to_plain_text_fragment(tail))
    return fragments


def visit_paragraph(
    element: Element,
    locator: DocLocator,
) -> DocParagraph:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoTail(element, locator)
    return {
        "type": "paragraph",
        "location": locator,
        "content": visit_fragment_container(element),
    }


def visit_figure(
    element: Element,
    locator: DocLocator,
) -> DocFigure:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoText(element, locator)
    assertNoTail(element, locator)
    children = list_html_children(element)
    if len(children) > 2:
        raise ValueError(
            f"Expected figure at {locator} to have at most 2 children: <img> and <figcaption>, got: {len(children)}"
        )
    child1 = children[0] if len(children) > 0 else None
    child2 = children[1] if len(children) > 1 else None
    if child1 is None or get_html_tag(child1) != "img":
        raise ValueError(
            f"Expected first child of figure at {locator} to be <img>"
        )
    return {
        "type": "figure",
        "location": locator,
        "source": get_html_attr(child1, "src"),
        "caption": (
            visit_fragment_container(child2) if child2 is not None else None
        ),
    }


def get_language_from_class(class_str: str | None) -> str | None:
    if class_str is None:
        return None
    if class_str.startswith("language-"):
        return class_str[len("language-") :]
    return None


def visit_listing(
    element: Element,
    locator: DocLocator,
) -> DocListing:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoText(element, locator)
    assertNoTail(element, locator)
    children = list_html_children(element)
    if len(children) != 1:
        raise ValueError(
            f"Expected listing at {locator} to have exactly 1 child: <code> with a <figcaption>, got: {len(children)}"
        )
    (child,) = children
    if get_html_tag(child) != "code":
        raise ValueError(f"Expected child of <pre> at {locator} to be <code>")
    text = get_html_text(child)
    if text is None:
        raise ValueError(f"Found empty text in listing context at {locator}")
    return {
        "type": "listing",
        "location": locator,
        "content": get_html_inner_text(element),
        "language": get_language_from_class(get_html_attr(child, "class")),
        "caption": None,
    }


def visit_table_cell(
    element: Element,
    locator: DocLocator,
) -> DocTableCell:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoTail(element, locator)
    return {
        "type": "table_cell",
        "location": locator,
        "content": visit_fragment_container(element),
    }


def visit_table_row(
    element: Element,
    locator: DocLocator,
) -> DocTableRow:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoText(element, locator)
    assertNoTail(element, locator)
    return {
        "type": "table_row",
        "location": locator,
        "columns": [
            visit_table_cell(child, locate_position(locator, index))
            for index, child in enumerate(iterate_html_children(element))
        ],
    }


def visit_table_part(
    element: Element,
    locator: DocLocator,
) -> list[DocTableRow]:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoText(element, locator)
    assertNoTail(element, locator)
    return [
        visit_table_row(
            child,
            locate_position(locator, index),
        )
        for index, child in enumerate(iterate_html_children(element))
    ]


def visit_table(
    element: Element,
    locator: DocLocator,
) -> DocTable:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoText(element, locator)
    assertNoTail(element, locator)
    table: DocTable = {
        "type": "table",
        "location": locator,
        "header": None,
        "rows": [],
        "footer": None,
        "caption": None,
    }
    for index, child in enumerate(iterate_html_children(element)):
        tag = get_html_tag(child)
        if tag == "caption":
            if table["caption"] is not None:
                raise ValueError(
                    f"Expected at most one <caption> in table at {locator}"
                )
            table["caption"] = visit_fragment_container(child)
        else:
            rows = visit_table_part(child, locate_position(locator, index))
            if tag == "thead":
                if table["header"] is not None:
                    raise ValueError(
                        f"Expected at most one <thead> in table at {locator}"
                    )
                if len(rows) != 1:
                    raise ValueError(
                        f"Expected exactly one row in <thead> at {locator}, got: {len(rows)}"
                    )
                table["header"] = rows[0]
            elif tag == "tbody":
                if table["rows"]:
                    raise ValueError(
                        f"Expected at most one <tbody> in table at {locator}"
                    )
                table["rows"] = rows
            elif tag == "tfoot":
                if table["footer"] is not None:
                    raise ValueError(
                        f"Expected at most one <tfoot> in table at {locator}"
                    )
                if len(rows) != 1:
                    raise ValueError(
                        f"Expected exactly one row in <tfoot> at {locator}, got: {len(rows)}"
                    )
                table["footer"] = rows[0]
    return table


def visit_list_item(
    element: Element,
    locator: DocLocator,
) -> DocListItem:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoTail(element, locator)
    return {
        "type": "list_item",
        "location": locator,
        "content": visit_fragment_container(element),
    }


def visit_list(
    element: Element,
    locator: DocLocator,
) -> DocList:
    locator = locate_element(
        locator,
        get_html_tag(element),
    )
    assertNoText(element, locator)
    assertNoTail(element, locator)
    return {
        "type": "list",
        "location": locator,
        "numbered": get_html_tag(element) == "ol",
        "items": [
            visit_list_item(child, locate_position(locator, index))
            for index, child in enumerate(iterate_html_children(element))
        ],
    }


def visit_container(
    element: Element,
    locator: DocLocator,
) -> list[DocSectionNode]:
    tag = get_html_tag(element)
    locator = locate_element(
        locator,
        tag,
    )
    if "alert" in (get_html_attr(element, "class") or ""):
        return [
            {
                "type": "paragraph",
                "location": locator,
                "content": visit_fragment_container(element),
            }
        ]
    else:
        children = list_html_children(element)
        nodes, remaining_index = visit_body(
            children,
            0,
            0,
            locator,
        )
        if remaining_index != len(children):
            raise ValueError(
                f"Expected to visit all children, but stopped at index {remaining_index} out of {len(children)} at {locator}"
            )
        return nodes


def visit_element(
    element: Element,
    locator: DocLocator,
) -> list[DocSectionNode]:
    tag: str = get_html_tag(element)
    if tag == "p":
        return [visit_paragraph(element, locator)]
    elif tag == "figure":
        return [visit_figure(element, locator)]
    elif tag == "pre":
        return [visit_listing(element, locator)]
    elif tag == "table":
        return [visit_table(element, locator)]
    elif tag in {"ul", "ol"}:
        return [visit_list(element, locator)]
    elif tag in {"div", "main"}:
        return visit_container(element, locator)
    else:
        raise ValueError(f"Unexpected tag: {tag} at {locator}")


HEADING_TAGS: set[str] = {"h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"}


def visit_body(
    elements: list[Element],
    index: int,
    depth: int,
    locator: DocLocator,
) -> Tuple[list[DocSectionNode], int]:
    nodes: list[DocSectionNode] = []
    while index < len(elements):
        element = elements[index]
        tag = get_html_tag(element)
        if tag in HEADING_TAGS:
            child_depth = int(tag[1:])
            if child_depth <= depth:
                return nodes, index
            else:
                children, remaining_index = visit_body(
                    elements,
                    index + 1,
                    child_depth,
                    locator,
                )
                nodes.append(
                    {
                        "type": "section",
                        "title": visit_fragment_container(element),
                        "location": locate_element(
                            locator,
                            tag,
                        ),
                        "title": visit_fragment_container(element),
                        "body": children,
                    }
                )
                index = remaining_index
        else:
            nodes.extend(
                visit_element(
                    element,
                    locate_position(locator, index),
                )
            )
            index += 1
    return nodes, index


def visit_page(element: Element, locator: DocLocator) -> list[DocSectionNode]:
    main = [
        *list_html_selector(element, ".//*[@class='doc-content']"),
        *list_html_selector(element, ".//*[@class='doc-article']"),
    ]
    if len(main) == 0:
        raise ValueError(
            f"Expected to find at least one element with class 'doc-content' or 'doc-article' in page at {locator}"
        )
    # doc-content class takes precedence over doc-article
    return visit_container(main[0], locator)


def parse_rapidscada_page(
    content: str, locator: DocLocator
) -> list[DocSectionNode]:
    root = parse_html(content)
    return visit_page(root, locator)
