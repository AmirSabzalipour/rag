from typing import Any
import time
import json
from scada_chatbot.extracting.__types__ import (
    ExtractionConfig,
    ExtractionSchema,
)
from scada_chatbot.extracting.openai import extract_openai


def extract(
    system: str,
    markdown: str,
    schema: ExtractionSchema,
    config: ExtractionConfig,
) -> Any:
    id = int(10e6 * time.time())
    print(f"Extracting with config: { {**config, 'api_key': '***'} }...")
    print(f"System Prompt: {system.splitlines()[0][0:100]}...")
    print(f"Markdown: {markdown.splitlines()[0][0:100]}...")
    with open(f"logs/{id}-1-config.json", "w") as file:
        json.dump({**config, "api_key": "***"}, file, indent=2)
    with open(f"logs/{id}-2-system.txt", "w") as file:
        file.write(system)
    with open(f"logs/{id}-3-input.md", "w") as file:
        file.write(markdown)
    with open(f"logs/{id}-4-schema.json", "w") as file:
        json.dump(schema, file, indent=2)
    response = extract_inner(
        system=system,
        markdown=markdown,
        schema=schema,
        config=config,
    )
    with open(f"logs/{id}-5-response.json", "w") as file:
        json.dump(response, file, indent=2)
    return response


def extract_inner(
    system: str,
    markdown: str,
    schema: ExtractionSchema,
    config: ExtractionConfig,
) -> Any:
    if config["type"] == "openai":
        return extract_openai(
            system=system,
            markdown=markdown,
            schema=schema,
            api_key=config["api_key"],
            model_name=config["model_name"],
            reasoning_effort=config["reasoning_effort"],
        )
    else:
        raise UnreachableError(config)
