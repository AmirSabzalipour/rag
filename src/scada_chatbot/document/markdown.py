from scada_chatbot.document.__types__ import (
    DocFigure,
    DocFragment,
    DocList,
    DocListItem,
    DocListing,
    DocParagraph,
    DocSection,
    DocSectionNode,
    DocTable,
    DocTableCell,
    DocTableRow,
    DocText,
)
from scada_chatbot.utils import UnreachableError


def mdify_fragment(fragment: DocFragment) -> str:
    if fragment["type"] == "link":
        content = fragment["content"]
        link = fragment["link"]
        return f"[{content}]({link})"
    else:
        content = fragment["content"]
        style = fragment["style"]
        if style == "none":
            return content
        elif style == "emph":
            return f"*{content}*"
        elif style == "strong":
            return f"**{content}**"
        elif style == "code":
            return f"`{content}`"
        else:
            raise UnreachableError(style)


def mdify_text(text: DocText) -> str:
    return " ".join(mdify_fragment(fragment) for fragment in text)


def mdify_paragraph(paragraph: DocParagraph) -> str:
    return mdify_text(paragraph["content"])


def mdify_section(section: DocSection, depth: int) -> str:
    title = mdify_text(section["title"])
    body = "\n\n".join(
        mdify_section_node(node, depth + 1) for node in section["body"]
    )
    return f"{'#' * depth} {title}\n\n{body}"


def mdify_table_cell(cell: DocTableCell) -> str:
    return mdify_text(cell["content"]).strip()


def mdify_table_row(row: DocTableRow) -> str:
    return (
        "| "
        + " | ".join(mdify_table_cell(cell) for cell in row["columns"])
        + " |"
    )


def mdify_table(table: DocTable) -> str:
    header = table["header"]
    rows = table["rows"]
    footer = table["footer"]
    num_cols = max(
        len(header) if header else 0,
        max((len(row["columns"]) for row in rows), default=0),
        len(footer) if footer else 0,
    )
    header_row = None if header is None else mdify_table_row(header)
    separator_row = "| " + " | ".join("---" for _ in range(num_cols)) + " |"
    main_rows = "\n".join(mdify_table_row(row) for row in rows)
    footer_row = None if footer is None else mdify_table_row(footer)
    return "\n".join(
        filter(None, [header_row, separator_row, main_rows, footer_row])
    )


def mdify_figure(figure: DocFigure) -> str:
    caption = mdify_text(figure["caption"]) if figure["caption"] else ""
    source = figure["source"] or ""
    return f"![{caption}]({source})"


def mdify_list_item(item: DocListItem, index: int | None) -> str:
    prefix = f"{index+1}. " if index is not None else "- "
    return prefix + mdify_text(item["content"])


def mdify_list(list_node: DocList) -> str:
    items = "\n".join(
        mdify_list_item(item, index if list_node["numbered"] else None)
        for index, item in enumerate(list_node["items"])
    )
    return items


def mdify_listing(listing: DocListing) -> str:
    caption = mdify_text(listing["caption"]) if listing["caption"] else ""
    language = listing["language"] or ""
    content = listing["content"]
    return f"```{language}\n{content}\n```\n\n{caption}"


def mdify_section_node(node: DocSectionNode, depth: int) -> str:
    if node["type"] == "paragraph":
        return mdify_paragraph(node)
    elif node["type"] == "section":
        return mdify_section(node, depth)
    elif node["type"] == "table":
        return mdify_table(node)
    elif node["type"] == "figure":
        return mdify_figure(node)
    elif node["type"] == "list":
        return mdify_list(node)
    elif node["type"] == "listing":
        return mdify_listing(node)
    else:
        raise UnreachableError(node)


def to_markdown(nodes: list[DocSection]) -> str:
    return "\n\n".join(mdify_section_node(node, 1) for node in nodes)
