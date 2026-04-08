import hashlib
from scada_chatbot.entity.__types__ import (
    Entity,
    EntityAppearance,
    EntityAttribute,
)
from scada_chatbot.embeding.__types__ import Embedding


def make_entity(
    labels: set[str],
    attributes: dict[str, EntityAttribute],
    appearances: list[EntityAppearance],
    embedding: Embedding,
) -> Entity:
    unique = "|".join(
        sorted(
            f"{appearance['location']}:{appearance['position']}"
            for appearance in appearances
        )
    )
    hash = hashlib.sha256(unique.encode()).hexdigest()
    return {
        "id": hash,
        "labels": labels,
        "attributes": attributes,
        "appearances": appearances,
        "embedding": embedding,
    }
