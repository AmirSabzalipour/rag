from typing import Literal, TypedDict

import numpy as np

Embedding = np.typing.NDArray[np.float32]

HuggingEmbeddingModel = Literal["BAAI/bge-base-en-v1.5"]

OpenaiEmbeddingModel = Literal["text-embedding-3-small"]


class HuggingEmbeddingConfig(TypedDict):
    type: Literal["hugging"]
    model_name: HuggingEmbeddingModel
    batch_size: int


class OpenAIEmbeddingConfig(TypedDict):
    type: Literal["openai"]
    model_name: OpenaiEmbeddingModel
    batch_size: int
    api_key: str


EmbeddingConfig = HuggingEmbeddingConfig | OpenAIEmbeddingConfig
