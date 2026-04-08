from typing import Any
from jsonschema import validate
from openai import OpenAI
from scada_chatbot import (
    knowledge,
)
import os
import json
import re

JSONSchema = dict[str, object]


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

non_word_re = re.compile(r"\W+")

multi_underscore_re = re.compile(r"_+")


with open("schemas/entities.json", "r") as file:
    entities_schema: JSONSchema = json.load(file)

with open("schemas/relationships.json", "r") as file:
    relationships_schema: JSONSchema = json.load(file)


def extract(
    model: str,
    name: str,
    description: str,
    schema: JSONSchema,
    temperature: float,
    prompt: str,
) -> Any:
    response = client.chat.completions.create(
        model=model,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": name,
                "description": description,
                "schema": schema,
                "strict": True,
            },
        },
        messages=[
            {
                "role": "system",
                "content": "You are an expert in SCADA systems and entity relationship extraction.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    if len(response.choices) == 0:
        raise ValueError("No response from the model")
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from the model")
    data = json.loads(content)
    validate(instance=data, schema=schema)
    return data


def prompt_extract_entities(text: str) -> str:
    return "\n".join(
        [
            "Extract all entities from the following SCADA documentation paragraph.",
            "Return the result as a JSON object with an 'entities' field.",
            "",
            "Paragraph:",
            f'"""{text}"""',
        ]
    )


def extract_entities(
    model: str,
    text: str,
    temperature: float,
) -> list[knowledge.RawEntity]:
    return extract(
        model=model,
        name="entities_extraction",
        description="List of entities extracted from SCADA documentation suitable for the nodes of a knowledge graph.",
        schema=entities_schema,
        prompt=prompt_extract_entities(text),
        temperature=temperature,
    )["entities"]


def prompt_extract_relationships(
    entities: list[knowledge.Entity], text: str
) -> str:
    return "\n".join(
        [
            "Given the following list of entities and a SCADA documentation paragraph, extract all relationships between the entities.",
            "Return the result as a JSON object with a 'relationships' field.",
            "",
            "Entities:",
            *[
                f"- {entity['id']} (\"{entity['name']}\") of type {entity['type']}"
                for entity in entities
            ],
            "",
            "Paragraph:",
            f'"""{text}"""',
        ]
    )


def sanitize_component(component: str) -> str:
    component = component.strip().lower()
    component = non_word_re.sub("_", component)
    component = multi_underscore_re.sub("_", component)
    return component.strip("_")


def make_entity_id(name: str, type: knowledge.EntityType) -> knowledge.EntityID:
    return knowledge.EntityID(
        f"{sanitize_component(type)}:{sanitize_component(name)}"
    )


def sanitize_attributes(
    attributes: knowledge.Attributes,
) -> knowledge.Attributes:
    return {sanitize_component(key): value for key, value in attributes.items()}


def cook_entity(entity: knowledge.RawEntity) -> knowledge.Entity:
    return {
        "id": make_entity_id(entity["name"], entity["type"]),
        "name": entity["name"],
        "type": entity["type"],
        "attributes": sanitize_attributes(entity.get("attributes", {}) or {}),
    }


def cook_relationship(
    relationship: knowledge.RawRelationship, entities: list[knowledge.Entity]
) -> knowledge.Relationship:
    return {
        "source": relationship["source"],
        "target": relationship["target"],
        "type": relationship["type"],
        "attributes": sanitize_attributes(
            relationship.get("attributes", {}) or {}
        ),
    }


def extract_relationships(
    model: str,
    entities: list[knowledge.Entity],
    text: str,
    temperature: float,
) -> list[knowledge.RawRelationship]:
    return extract(
        model=model,
        name="relationships_extraction",
        description="List of relationships between entities extracted from SCADA documentation suitable for the edges of a knowledge graph.",
        schema=relationships_schema,
        prompt=prompt_extract_relationships(entities, text),
        temperature=temperature,
    )["relationships"]


scada_paragraph = """
The Pump Station contains three pumps (Pump A, Pump B, Pump C) and two sensors (Pressure Sensor, Flow Sensor). 
Each pump is controlled by a PLC, and the sensors provide real-time data to the SCADA system. 
The SCADA system monitors the status of all pumps and sensors, and can send commands to the PLCs to start or stop the pumps.
"""

raw_entities = extract_entities(
    model="gpt-4.1-mini",
    text=scada_paragraph,
    temperature=0,
)

entities = [cook_entity(raw_entity) for raw_entity in raw_entities]

raw_relationships = extract_relationships(
    model="gpt-4.1-mini",
    entities=entities,
    text=scada_paragraph,
    temperature=0,
)

relationships = [
    cook_relationship(raw_relationship, entities)
    for raw_relationship in raw_relationships
]

print(
    json.dumps({"entities": entities, "relationships": relationships}, indent=2)
)
