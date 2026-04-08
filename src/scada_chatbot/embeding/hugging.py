import numpy as np
from sentence_transformers import SentenceTransformer
from scada_chatbot.embeding.__types__ import Embedding, HuggingEmbeddingModel
from scada_chatbot.utils import UnreachableError


transformers: dict[HuggingEmbeddingModel, SentenceTransformer] = {}


def get_hugging_embedding_prefix(model_name: HuggingEmbeddingModel) -> str:
    if model_name == "BAAI/bge-base-en-v1.5":
        return "Represent this sentence for retrieval: "
    raise UnreachableError(model_name)


def get_hugging_embedding_dimension(model_name: HuggingEmbeddingModel) -> int:
    if model_name == "BAAI/bge-base-en-v1.5":
        return 768
    raise UnreachableError(model_name)


def embed_hugging(
    input: list[str],
    model_name: HuggingEmbeddingModel,
) -> list[Embedding]:
    if model_name not in transformers:
        transformers[model_name] = SentenceTransformer(model_name)
    transformer = transformers[model_name]
    prefix = get_hugging_embedding_prefix(model_name)
    sentences = [prefix + sentence for sentence in input]
    embeddings = transformer.encode(
        sentences,
        convert_to_numpy=True,
        normalize_embeddings=True,  # Required for cosine search
    )
    return [emb.astype(np.float32) for emb in embeddings]
