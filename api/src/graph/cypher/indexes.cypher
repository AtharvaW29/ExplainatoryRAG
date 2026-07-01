CREATE INDEX concept_description
IF NOT EXISTS
FOR (c:Concept)
ON (c.description);
