UNWIND $ENTITIES AS ENTITY
MERGE (entity:_ENTITY_LABELS_:Entity {id: ENTITY.id})
SET entity.embedding = ENTITY.embedding
SET entity += ENTITY.attributes

WITH entity, ENTITY
UNWIND ENTITY.appearance AS APPEARANCE
MERGE (document:Document {location: APPEARANCE.location})
MERGE (document)-[relationship:MENTIONS]->(entity)
SET relationship.position = APPEARANCE.position
SET relationship.name = APPEARANCE.name
SET relationship.description = APPEARANCE.description