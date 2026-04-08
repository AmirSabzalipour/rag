from typing import LiteralString, cast

from scada_chatbot.entity.__types__ import Entity
from scada_chatbot.queries.__types__ import ParamQuery


with open("src/scada_chatbot/queries/insert_entity.template.cql", "r") as file:
    INSERT_ENTITIES_QUERY_TEMPLATE = file.read()


def hash_entity_labels(labels: set[str]) -> str:
    if not all(label.isidentifier() for label in labels):
        raise ValueError("Entity types must be valid identifiers")
    return "".join([":" + label for label in sorted(labels)])


def list_insert_entities_query(
    entities: list[Entity],
) -> list[ParamQuery]:
    by_labels: dict[str, list[Entity]] = {}
    for entity in entities:
        label = hash_entity_labels(entity["labels"])
        if label not in by_labels:
            by_labels[label] = []
        by_labels[label].append(entity)
    return [
        {
            "query": cast(
                LiteralString,
                INSERT_ENTITIES_QUERY_TEMPLATE.replace(
                    ":_ENTITY_LABELS_",
                    labels,
                ),
            ),
            "params": {
                "ENTITIES": [
                    {
                        "id": entity["id"],
                        "embedding": entity["embedding"].tolist(),
                        "attributes": entity["attributes"],
                        "appearances": entity["appearances"],
                    }
                    for entity in entities
                ],
            },
        }
        for labels, entities in by_labels.items()
    ]
