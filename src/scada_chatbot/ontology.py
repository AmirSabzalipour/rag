import json
from typing import TypedDict


class EntityTypeSpec(TypedDict):
    description: str


class RelationshipTypeSpec(TypedDict):
    description: str
    source_types: list[str]
    target_types: list[str]


class Ontology(TypedDict):
    entity_types: dict[str, EntityTypeSpec]
    relationship_types: dict[str, RelationshipTypeSpec]


with open("ontology.json", "r") as file:
    ONTOLOGY: Ontology = json.load(file)
