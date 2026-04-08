WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "section"
MERGE (d:Document:Section {location: NODE.source})
SET d.title = NODE.title

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "paragraph"
MERGE (d:Document:Paragraph {location: NODE.source})
SET d.content = NODE.content

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "figure"
MERGE (d:Document:Figure {location: NODE.sourcem})
SET d.caption = NODE.caption
SET d.source = NODE.source

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "listing"
MERGE (d:Document:Listing {location: NODE.source})
SET d.caption = NODE.caption
SET d.content = NODE.content

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "table"
MERGE (d:Document:Table {location: NODE.source})
SET d.caption = NODE.caption

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "table_row"
MERGE (d:Document:TableRow {location: NODE.source})

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "table_cell"
MERGE (d:Document:TableCell {location: NODE.source})
SET d.content = NODE.content

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "list"
MERGE (d:Document:List {location: NODE.source})
SET d.numbered = NODE.numbered

WITH 1 AS dummy
UNWIND $NODES AS NODE
WITH NODE
WHERE NODE.type = "list_item"
MERGE (d:Document:ListItem {location: NODE.source})
SET d.content = NODE.content

WITH 1 AS dummy
UNWIND $RELATIONSHIPS AS RELATIONSHIP
MATCH (source:Document {location: RELATIONSHIP.source})
MATCH (target:Document {location: RELATIONSHIP.target})
MERGE (source)-[relationship:CONTAINS {type: RELATIONSHIP.type}]->(target)
SET relationship.position = RELATIONSHIP.position