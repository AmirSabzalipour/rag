from typing import Literal, TypedDict

from openai.types import ChatModel, ReasoningEffort


class OpenaiExtractionConfig(TypedDict):
    type: Literal["openai"]
    api_key: str
    model_name: ChatModel
    reasoning_effort: ReasoningEffort


ExtractionConfig = OpenaiExtractionConfig


class ExtractionSchema(TypedDict):
    name: str
    description: str
    content: dict
