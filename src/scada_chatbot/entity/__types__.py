from typing import TypedDict
from scada_chatbot.embeding.__types__ import Embedding


class Mention(TypedDict):
    location: str
    position: int


class MentionRelationship(TypedDict):
    source: str
    target: str


class ExtractAttribute(TypedDict):
    name: str
    description: str
    value: bool | int | float | str


class ExtractEntity(TypedDict):
    type: str
    name: str
    description: str
    attributes: list[ExtractAttribute]


class ExtractRelationship(TypedDict):
    type: str
    source: str
    target: str


class SemanticRelationship(TypedDict):
    type: str
    source: str
    target: str


class EntityAnchor(TypedDict):
    id: str
    name: str
    description: str


class EntityAttribute(TypedDict):
    description: str
    value: bool | int | float | str


class EntityAppearance(TypedDict):
    name: str
    description: str
    location: str
    position: int


class Entity(TypedDict):
    id: str
    labels: set[str]
    attributes: dict[str, EntityAttribute]
    appearances: list[EntityAppearance]
    embedding: Embedding
