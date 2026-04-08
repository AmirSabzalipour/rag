from scada_chatbot.document.__types__ import DocLocator


def make_root_locator(
    path: str,
) -> DocLocator:
    return DocLocator(path)


def locate_element(
    locator: DocLocator,
    tag: str,
) -> DocLocator:
    return DocLocator(f"{locator}[{tag}]")


def locate_position(
    locator: DocLocator,
    index: int,
) -> DocLocator:
    return DocLocator(f"{locator}/{index}")
