import os

from scada_chatbot.document.__types__ import DocSection
from scada_chatbot.embeding import get_embedding_dimension
from scada_chatbot.embeding.__types__ import EmbeddingConfig
from scada_chatbot.entity.__types__ import (
    Entity,
    SemanticRelationship,
)
from scada_chatbot.entity.cluster import cluster_entities_by_similarity
from scada_chatbot.entity.embed import embed_entities
from scada_chatbot.entity.extract import (
    extract_entities,
    extract_semantic_relationships,
)
from scada_chatbot.entity.mention import derive_mention_relationships
from scada_chatbot.extracting.__types__ import ExtractionConfig
from scada_chatbot.document.markdown import mdify_section
from scada_chatbot.database import DatabaseConnection, execute_query
from scada_chatbot.ontology import ONTOLOGY, Ontology
from scada_chatbot.queries.insert_document import make_insert_document_query
from scada_chatbot.queries.insert_entity import list_insert_entities_query
from scada_chatbot.queries.insert_semantic_relationship import (
    list_insert_semantic_relationships_query,
)
from scada_chatbot.queries.setup import make_setup_query
from scada_chatbot.rapid_scada import (
    chunk_rapid_scada_documentation,
    load_rapid_scada_documentation,
)


def load_entities(
    sections: list[DocSection],
    ontology: Ontology,
    similarity_threshold: float,
    embedding_config: EmbeddingConfig,
    extraction_config: ExtractionConfig,
) -> list[Entity]:
    entities = [
        entity
        for section in sections
        for entity in extract_entities(
            mdify_section(section, depth=0),
            location=section["location"],
            ontology=ontology,
            config=extraction_config,
        )
    ]
    entities = embed_entities(
        entities,
        config=embedding_config,
    )
    entities = cluster_entities_by_similarity(
        entities,
        similarity_threshold=similarity_threshold,
    )
    return entities


def load_semantic_relationships(
    section: DocSection,
    entities: list[Entity],
    ontology: Ontology,
    extraction_config: ExtractionConfig,
) -> list[SemanticRelationship]:
    return extract_semantic_relationships(
        mdify_section(section, depth=0),
        anchors=[
            {
                "id": entity["id"],
                "name": appearance["name"],
                "description": appearance["description"],
            }
            for entity in entities
            for appearance in entity["appearances"]
            if appearance["location"] == section["location"]
        ],
        ontology=ontology,
        config=extraction_config,
    )


def main():
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    OPENAI_MODEL_NAME = "gpt-5.2"
    OPENAI_REASONING_EFFORT = "none"
    SIMILARITY_THRESHOLD = 0.85
    EMBEDDING_CONFIG: EmbeddingConfig = {
        "type": "hugging",
        "model_name": "BAAI/bge-base-en-v1.5",
        "batch_size": 64,
    }
    EXTRACTION_CONFIG: ExtractionConfig = {
        "type": "openai",
        "api_key": OPENAI_API_KEY,
        "model_name": OPENAI_MODEL_NAME,
        "reasoning_effort": OPENAI_REASONING_EFFORT,
    }
    CONNECTION: DatabaseConnection = {
        "uri": "neo4j+s://localhost:7687",
        "user": "neo4j",
        "password": "password",
        "database": "neo4j",
    }
    EMBEDDING_DIMENSION = get_embedding_dimension(EMBEDDING_CONFIG)
    documentation = load_rapid_scada_documentation()
    chunks = chunk_rapid_scada_documentation(documentation)
    entities = load_entities(
        sections=chunks,
        ontology=ONTOLOGY,
        similarity_threshold=SIMILARITY_THRESHOLD,
        embedding_config=EMBEDDING_CONFIG,
        extraction_config=EXTRACTION_CONFIG,
    )
    semantic_relationships = [
        relationship
        for section in chunks
        for relationship in load_semantic_relationships(
            section=section,
            entities=entities,
            ontology=ONTOLOGY,
            extraction_config=EXTRACTION_CONFIG,
        )
    ]
    execute_query(
        connection=CONNECTION,
        param_query=make_setup_query(embedding_dimension=EMBEDDING_DIMENSION),
    )
    execute_query(
        connection=CONNECTION,
        param_query=make_insert_document_query(documentation),
    )
    for param_query in list_insert_entities_query(entities):
        execute_query(
            connection=CONNECTION,
            param_query=param_query,
        )
    for param_query in list_insert_semantic_relationships_query(
        semantic_relationships
    ):
        execute_query(
            connection=CONNECTION,
            param_query=param_query,
        )


if __name__ == "__main__":
    main()
