# This is not currently used, but is kept as a reference

from typing import TypedDict
from typing_extensions import Literal

from openai.types import Embedding

from scada_chatbot.document.markdown import mdify_text
from scada_chatbot.document.__types__ import (
    DocFigure,
    DocListing,
    DocLocator,
    DocParagraph,
    DocTableCell,
    DocTableRow,
    DocText,
)


class EmbeddedDocParagraph(DocParagraph):
    embedding: Embedding


class EmbeddedDocFigure(DocFigure):
    embedding: Embedding


class EmbeddedDocListing(DocListing):
    embedding: Embedding


class EmbeddedDocTableRow(DocTableRow):
    embedding: Embedding


class EmbeddedDocTable(TypedDict):
    type: Literal["table"]
    origin: DocLocator
    caption: DocText | None
    embedding: Embedding
    header: EmbeddedDocTableRow | None
    main: list[EmbeddedDocTableRow]
    footer: EmbeddedDocTableRow | None


EmbeddedDocNode = (
    EmbeddedDocParagraph
    | EmbeddedDocFigure
    | EmbeddedDocListing
    | EmbeddedDocTable
)


class EmbeddedDocSection(TypedDict):
    type: Literal["section"]
    origin: DocLocator
    title: DocText
    embedding: Embedding
    body: list[EmbeddedDocNode]


def describe_table_cell(
    head: DocTableCell,
    cell: DocTableCell,
) -> str:
    key = ("" if head is None else mdify_text(head["content"])).strip()
    val = mdify_text(cell["content"]).strip()
    return f"{key}: {val}" if key else val


def describe_table_row(
    row: DocTableRow,
    header: None | DocTableRow,
) -> str:
    columns = row["columns"]
    heads: list[DocTableCell] = []
    if header is not None:
        heads = header["columns"][0 : len(columns)]
    while len(heads) < len(columns):
        heads.append(
            {
                "type": "table_cell",
                "location": row["location"],
                "content": [],
            }
        )
    return "\n".join(
        describe_table_cell(head, cell) for head, cell in zip(heads, columns)
    )
