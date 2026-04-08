from collections.abc import Iterator

from scada_chatbot.document.__types__ import DocNode


def iter_doc_children(
    node: DocNode,
    depth: int,
) -> Iterator[DocNode]:
    if depth != 0:
        depth -= 1
        yield node
        if depth > 0:
            if node["type"] == "section":
                for child in node["body"]:
                    yield from iter_doc_children(child, depth)
            elif node["type"] == "list":
                for child in node["items"]:
                    yield from iter_doc_children(child, depth)
            elif node["type"] == "table":
                if node["header"]:
                    yield from iter_doc_children(node["header"], depth)
                for child in node["rows"]:
                    yield from iter_doc_children(child, depth)
                if node["footer"]:
                    yield from iter_doc_children(node["footer"], depth)
