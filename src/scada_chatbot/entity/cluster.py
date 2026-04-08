import numpy as np
from sklearn.cluster import DBSCAN

from scada_chatbot.embeding.__types__ import Embedding
from scada_chatbot.entity.__types__ import Entity
from scada_chatbot.entity.entity import make_entity

EPS = 1e-6


def average_embedding(embeddings: list[Embedding]) -> Embedding:
    embedding = np.mean(embeddings, axis=0)
    norm = np.linalg.norm(embedding)
    return embedding / (norm + EPS)


def cluster_entities_by_similarity(
    entities: list[Entity],
    similarity_threshold: float,
) -> list[Entity]:
    for entity in entities:
        norm = np.linalg.norm(entity["embedding"])
        if not (1 - EPS < norm < 1 + EPS):
            raise ValueError("Entity embedding is not normalized")
    db = DBSCAN(
        eps=similarity_threshold,
        min_samples=1,
        metric="cosine",
    )
    labels = db.fit_predict(
        np.stack([entity["embedding"] for entity in entities]),
    )
    clusters: dict[int, list[Entity]] = {}
    for index, label in enumerate(labels):
        clusters.setdefault(label, []).append(entities[index])
    return [collapse_entity_cluster(cluster) for cluster in clusters.values()]


def collapse_entity_cluster(
    entities: list[Entity],
) -> Entity:
    return make_entity(
        labels=set(label for entity in entities for label in entity["labels"]),
        attributes={
            name: attribute
            for entity in entities
            for name, attribute in entity["attributes"].items()
        },
        appearances=[
            appearance
            for entity in entities
            for appearance in entity["appearances"]
        ],
        embedding=average_embedding(
            [entity["embedding"] for entity in entities]
        ),
    )
