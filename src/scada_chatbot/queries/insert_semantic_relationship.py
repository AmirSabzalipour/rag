from typing import LiteralString, cast

from scada_chatbot.entity.__types__ import SemanticRelationship
from scada_chatbot.queries.__types__ import ParamQuery


with open(
    "src/scada_chatbot/queries/insert_semantic_relationship.template.cql", "r"
) as file:
    INSERT_RELATIONSHIPS_QUERY_TEMPLATE = file.read()


def hash_relationship_type(type: str) -> str:
    if not type.isidentifier():
        raise ValueError("Relationship type must be a valid identifier")
    return ":" + type


def list_insert_semantic_relationships_query(
    relationships: list[SemanticRelationship],
) -> list[ParamQuery]:
    by_type: dict[str, list[SemanticRelationship]] = {}
    for relationship in relationships:
        type = hash_relationship_type(relationship["type"])
        if type not in by_type:
            by_type[type] = []
        by_type[type].append(relationship)
    return [
        {
            "query": cast(
                LiteralString,
                INSERT_RELATIONSHIPS_QUERY_TEMPLATE.replace(
                    ":_RELATIONSHIP_TYPE_", type
                ),
            ),
            "params": {"RELATIONSHIPS": relationships},
        }
        for type, relationships in by_type.items()
    ]
