from scada_chatbot.embeding.__types__ import Embedding, EmbeddingConfig
from scada_chatbot.utils import UnreachableError, group
from scada_chatbot.embeding.hugging import (
    embed_hugging,
    get_hugging_embedding_dimension,
)
from scada_chatbot.embeding.openai import (
    embed_openai,
    get_openai_embedding_dimension,
)


def embed(
    input: list[str],
    config: EmbeddingConfig,
) -> list[Embedding]:
    embeddings = []
    for batch in group(input, config["batch_size"]):
        print(f"Embedding batch of size {len(batch)}...")
        embeddings.append(embed_batch(batch, config))
    return embeddings


def embed_batch(
    input: list[str],
    config: EmbeddingConfig,
) -> list[Embedding]:
    if config["type"] == "openai":
        return embed_openai(
            input,
            model_name=config["model_name"],
            api_key=config["api_key"],
        )
    elif config["type"] == "hugging":
        return embed_hugging(
            input,
            model_name=config["model_name"],
        )
    else:
        raise UnreachableError(config)


def get_embedding_dimension(config: EmbeddingConfig) -> int:
    if config["type"] == "openai":
        return get_openai_embedding_dimension(config["model_name"])
    elif config["type"] == "hugging":
        return get_hugging_embedding_dimension(config["model_name"])
    else:
        raise UnreachableError(config)
