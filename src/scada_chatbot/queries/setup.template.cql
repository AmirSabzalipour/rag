CREATE CONSTRAINT document_location_unique IF NOT EXISTS
FOR (document:Document)
REQUIRE document.location IS UNIQUE;

CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (entity:Entity)
REQUIRE entity.id IS UNIQUE;

CREATE VECTOR INDEX entity_embedding_index IF NOT EXISTS FOR (entity:Entity) ON (entity.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: _EMBEDDING_DIMENSION_,
    `vector.similarity_function`: 'cosine'
  }
};