import numpy as np

from scada_chatbot.embeding import embed
from scada_chatbot.embeding.__types__ import EmbeddingConfig
from scada_chatbot.entity.__types__ import Entity


def embed_entities(
    entities: list[Entity],
    config: EmbeddingConfig,
) -> list[Entity]:
    embeddings = embed(
        [
            "\n".join(
                f"{appearance['name']}: {appearance['description']}"
                for appearance in entity["appearances"]
            )
            for entity in entities
        ],
        config,
    )
    return [
        {
            **entity,
            "embedding": np.array(embedding, dtype=np.float32),
        }
        for entity, embedding in zip(entities, embeddings)
    ]
