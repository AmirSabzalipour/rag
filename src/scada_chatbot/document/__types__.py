from typing import TypedDict, Literal, NewType


DocLocator = NewType("DocLocator", str)


DocFragmentStyle = Literal["none", "emph", "strong", "code"]


class DocLinkFragment(TypedDict):
    type: Literal["link"]
    link: str
    content: str


class DocTextFragment(TypedDict):
    type: Literal["text"]
    style: DocFragmentStyle
    content: str


DocFragment = DocLinkFragment | DocTextFragment


DocText = list[DocFragment]


class DocParagraph(TypedDict):
    type: Literal["paragraph"]
    location: DocLocator
    content: DocText


class DocSection(TypedDict):
    type: Literal["section"]
    location: DocLocator
    title: DocText
    body: list[DocSectionNode]


class DocListing(TypedDict):
    type: Literal["listing"]
    location: DocLocator
    content: str
    caption: DocText | None
    language: str | None


class DocListItem(TypedDict):
    type: Literal["list_item"]
    location: DocLocator
    content: DocText


class DocList(TypedDict):
    type: Literal["list"]
    location: DocLocator
    numbered: bool
    items: list[DocListItem]


class DocFigure(TypedDict):
    type: Literal["figure"]
    location: DocLocator
    source: str | None
    caption: DocText | None


class DocTableCell(TypedDict):
    type: Literal["table_cell"]
    location: DocLocator
    content: DocText


class DocTableRow(TypedDict):
    type: Literal["table_row"]
    location: DocLocator
    columns: list[DocTableCell]


class DocTable(TypedDict):
    type: Literal["table"]
    location: DocLocator
    caption: DocText | None
    header: DocTableRow | None
    rows: list[DocTableRow]
    footer: DocTableRow | None


DocSectionNode = (
    DocParagraph | DocSection | DocTable | DocFigure | DocList | DocListing
)

DocNode = (
    DocParagraph
    | DocSection
    | DocTable
    | DocFigure
    | DocList
    | DocListing
    | DocTableRow
    | DocListItem
)
