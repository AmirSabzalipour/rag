from scada_chatbot.document.__types__ import DocSection, DocSectionNode
from scada_chatbot.document.locator import make_root_locator
from scada_chatbot.rapid_scada.parse import parse_rapidscada_page
from scada_chatbot.rapid_scada.layout import LAYOUT, ROOT_DIR


def load_rapid_scada_documentation() -> DocSection:
    sections: list[DocSectionNode] = []
    for chapter in LAYOUT:
        locator = make_root_locator(chapter["url"])
        section: DocSection = {
            "type": "section",
            "title": [
                {
                    "type": "text",
                    "content": chapter["title"],
                    "style": "none",
                }
            ],
            "location": locator,
            "body": [],
        }
        for page in chapter["content"]:
            locator = make_root_locator(page)
            print(f"Loading {locator}...")
            with open(ROOT_DIR + page, "r", encoding="utf-8") as file:
                content = file.read()
            section["body"].extend(parse_rapidscada_page(content, locator))
        sections.append(section)
    return {
        "type": "section",
        "title": [
            {
                "type": "text",
                "content": "Rapid SCADA Documentation",
                "style": "none",
            }
        ],
        "location": make_root_locator(""),
        "body": sections,
    }


def chunk_rapid_scada_documentation(root: DocSection) -> list[DocSection]:
    pages: list[DocSection] = []
    for chapter in root["body"]:
        if chapter["type"] != "section":
            raise ValueError("Expected chapter to be a section")
        for page in chapter["body"]:
            if page["type"] != "section":
                raise ValueError("Expected page to be a section")
            pages.append(page)
    return pages
