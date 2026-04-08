from typing import Iterator, LiteralString, cast
from scada_chatbot.document.__types__ import DocNode
from scada_chatbot.document.utils import iter_doc_children
from scada_chatbot.queries.__types__ import ParamQuery, StructuralRelationship
from scada_chatbot.utils import UnreachableError


HEADER: int = -1
FOOTER: int = -2


with open("src/scada_chatbot/queries/insert_document.cql", "r") as file:
    INSERT_DOCUMENT_QUERY = file.read()


def iter_structural_relationships(
    node: DocNode,
) -> Iterator[StructuralRelationship]:
    if node["type"] == "section":
        for index, child in enumerate(node["body"]):
            yield {
                "position": index,
                "source": node["location"],
                "target": child["location"],
            }
            yield from iter_structural_relationships(child)
    elif node["type"] == "list":
        for index, child in enumerate(node["items"]):
            yield {
                "position": index,
                "source": node["location"],
                "target": child["location"],
            }
    elif node["type"] == "table":
        if node["header"]:
            yield {
                "position": HEADER,
                "source": node["location"],
                "target": node["header"]["location"],
            }
        for index, child in enumerate(node["rows"]):
            yield {
                "position": index,
                "source": node["location"],
                "target": child["location"],
            }
        if node["footer"]:
            yield {
                "position": FOOTER,
                "source": node["location"],
                "target": node["footer"]["location"],
            }
    elif node["type"] == "table_row":
        for index, child in enumerate(node["columns"]):
            yield {
                "position": index,
                "source": node["location"],
                "target": child["location"],
            }
    elif (
        node["type"] == "figure"
        or node["type"] == "image"
        or node["type"] == "listing"
        or node["type"] == "paragraph"
        or node["type"] == "table_cell"
        or node["type"] == "list_item"
    ):
        pass
    else:
        raise UnreachableError(node)


def make_insert_document_query(
    node: DocNode,
) -> ParamQuery:
    return {
        "query": cast(LiteralString, INSERT_DOCUMENT_QUERY),
        "params": {
            "NODES": list(iter_doc_children(node, depth=-1)),
            "RELATIONSHIPS": list(iter_structural_relationships(node)),
        },
    }
