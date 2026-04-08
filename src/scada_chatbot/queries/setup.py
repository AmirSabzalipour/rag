from typing import LiteralString, cast
from scada_chatbot.queries.__types__ import ParamQuery


with open("src/scada_chatbot/queries/setup.template.cql", "r") as file:
    SETUP_QUERY_TEMPLATE = file.read()


def make_setup_query(embedding_dimension: int) -> ParamQuery:
    return {
        "query": cast(
            LiteralString,
            SETUP_QUERY_TEMPLATE.replace(
                "_EMBEDDING_DIMENSION_", str(embedding_dimension)
            ),
        ),
        "params": {},
    }
