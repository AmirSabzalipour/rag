import json
from typing import Any
from openai import OpenAI
from openai.types import ChatModel, ReasoningEffort
from scada_chatbot.extracting.__types__ import ExtractionSchema

CLIENTS: dict[str, OpenAI] = {}


def extract_openai(
    system: str,
    markdown: str,
    schema: ExtractionSchema,
    api_key: str,
    model_name: ChatModel,
    reasoning_effort: ReasoningEffort,
) -> Any:
    if api_key not in CLIENTS:
        CLIENTS[api_key] = OpenAI(api_key=api_key)
    client = CLIENTS[api_key]
    response = client.chat.completions.create(
        model=model_name,
        reasoning_effort=reasoning_effort,
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": markdown,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema["name"],
                "description": schema["description"],
                "strict": True,
                "schema": schema["content"],
            },
        },
    )
    if not response.choices or not response.choices[0].message.content:
        raise ValueError("No content in response")
    return json.loads(response.choices[0].message.content)
