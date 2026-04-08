from typing import TypedDict

from neo4j import Driver, GraphDatabase

from scada_chatbot.queries.__types__ import ParamQuery


DRIVERS: dict[str, Driver] = {}


class DatabaseConnection(TypedDict):
    uri: str
    user: str
    password: str
    database: str


def hash_connection(connection: DatabaseConnection) -> str:
    return f"{connection['uri']}|{connection['user']}|{connection['password']}"


def connect(connection: DatabaseConnection) -> Driver:
    hash = hash_connection(connection)
    if hash not in DRIVERS:
        DRIVERS[hash] = GraphDatabase.driver(
            connection["uri"],
            auth=(
                connection["user"],
                connection["password"],
            ),
        )
    return DRIVERS[hash]


def execute_query(
    connection: DatabaseConnection,
    param_query: ParamQuery,
) -> None:
    driver = connect(connection)
    driver.execute_query(
        query_=param_query["query"],
        parameters_=param_query["params"],
        database_=connection["database"],
    )
