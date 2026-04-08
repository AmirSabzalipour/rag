from typing import LiteralString, TypedDict


class ParamQuery(TypedDict):
    query: LiteralString
    params: dict


class StructuralRelationship(TypedDict):
    position: int
    source: str
    target: str
