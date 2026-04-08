UNWIND $RELATIONSHIPS AS RELATIONSHIP
MATCH (source:Entity {id: RELATIONSHIP.source})
MATCH (target:Entity {id: RELATIONSHIP.target})
MERGE (source)-[:_RELATIONSHIP_TYPE_]->(target)