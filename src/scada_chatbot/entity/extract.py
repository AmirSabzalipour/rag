import json
import numpy as np
import warnings

from scada_chatbot.embeding.__types__ import Embedding
from scada_chatbot.entity.__types__ import (
    Entity,
    EntityAnchor,
    ExtractEntity,
    ExtractRelationship,
    SemanticRelationship,
)
from scada_chatbot.entity.entity import make_entity
from scada_chatbot.extracting import extract
from scada_chatbot.extracting.__types__ import ExtractionConfig
from scada_chatbot.ontology import Ontology


EMPTY_EMBEDDING: Embedding = np.zeros(0, dtype=np.float32)


with open("schemas/entities.json", "r") as file:
    ENTITIES_SCHEMA = json.load(file)


with open("schemas/relationships.json", "r") as file:
    RELATIONSHIPS_SCHEMA = json.load(file)


def extract_entities(
    markdown: str,
    location: str,
    ontology: Ontology,
    config: ExtractionConfig,
) -> list[Entity]:
    entities: list[ExtractEntity] = extract(
        system="\n".join(
            [
                "You are an assistant for extracting entities from technical SCADA documentation.",
                "Given a markdown document, you will extract the entities mentioned in the document.",
                "The available entity types are:",
                *[
                    f"- {key}: {val['description']}"
                    for key, val in ontology["entity_types"].items()
                ],
            ]
        ),
        markdown=markdown,
        schema={
            "name": "entities_extraction",
            "description": "SCADA Entities extraction schema",
            "content": ENTITIES_SCHEMA,
        },
        config=config,
    )["entities"]
    return [
        make_entity(
            labels=set(entity["type"]),
            attributes={
                attribute["name"]: {
                    "description": attribute["description"],
                    "value": attribute["value"],
                }
                for attribute in entity["attributes"]
            },
            appearances=[
                {
                    "name": entity["name"],
                    "description": entity["description"],
                    "location": location,
                    "position": index,
                }
            ],
            embedding=EMPTY_EMBEDDING,
        )
        for index, entity in enumerate(entities)
    ]


def extract_semantic_relationships(
    markdown: str,
    anchors: list[EntityAnchor],
    ontology: Ontology,
    config: ExtractionConfig,
) -> list[SemanticRelationship]:
    mapping: dict[str, str] = {
        anchor["name"]: anchor["id"] for anchor in anchors
    }
    relationships: list[ExtractRelationship] = extract(
        system="\n".join(
            [
                "You are an assistant for extracting relationships between entities from technical SCADA documentation."
                "Given a markdown document, you will extract the relationships mentioned in the document."
                "",
                "The available relationship types are:",
                *[
                    f"- {key}: {val['description']}"
                    for key, val in ontology["relationship_types"].items()
                ],
                "",
                "The available entities are:",
                *[
                    f"- {anchor['name']}: {anchor['description']}"
                    for anchor in anchors
                ],
            ]
        ),
        markdown=markdown,
        schema={
            "name": "relationships_extraction",
            "description": "SCADA Relationships extraction schema",
            "content": RELATIONSHIPS_SCHEMA,
        },
        config=config,
    )["relationships"]
    resolved_relationships: list[SemanticRelationship] = []
    for relationship in relationships:
        if relationship["source"] not in mapping:
            warnings.warn(
                f"Unknown entity '{relationship['source']}' in relationship extraction"
            )
            continue
        if relationship["target"] not in mapping:
            warnings.warn(
                f"Unknown entity '{relationship['target']}' in relationship extraction"
            )
            continue
        resolved_relationships.append(
            {
                "type": relationship["type"],
                "source": mapping[relationship["source"]],
                "target": mapping[relationship["target"]],
            }
        )
    return resolved_relationships
