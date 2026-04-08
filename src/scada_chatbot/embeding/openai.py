from openai import OpenAI
import tiktoken
from scada_chatbot.embeding.__types__ import Embedding, OpenaiEmbeddingModel
from scada_chatbot.utils import group
import numpy as np


CLIENTS: dict[str, OpenAI] = {}

OPENAI_EMBEDDING_MODEL: OpenaiEmbeddingModel = "text-embedding-3-small"

SENTENCE_DECREASE_FACTOR = 0.9

# Maximum openai tokens is 8192 but we use 4096 which should be plenty enough.
MAX_TOKEN_COUNT = 4096

ENCODING = tiktoken.get_encoding("cl100k_base")


def get_openai_embedding_dimension(model_name: OpenaiEmbeddingModel) -> int:
    if model_name == "text-embedding-3-small":
        return 1024
    else:
        raise UnreachableError(model_name)


def truncate(sentence: str) -> str:
    tokens = ENCODING.encode(sentence)
    if len(tokens) <= MAX_TOKEN_COUNT:
        return sentence
    else:
        tokens = tokens[:MAX_TOKEN_COUNT]
        return ENCODING.decode(tokens)


def embed_openai(
    input: list[str],
    api_key: str,
    model_name: OpenaiEmbeddingModel,
) -> list[Embedding]:
    if api_key not in CLIENTS:
        CLIENTS[api_key] = OpenAI(api_key=api_key)
    client = CLIENTS[api_key]
    response = client.embeddings.create(
        input=[truncate(sentence) for sentence in input],
        model=model_name,
    )
    if not response.data:
        raise ValueError("No data in response")
    return [
        np.array(item.embedding, dtype=np.float32) for item in response.data
    ]
