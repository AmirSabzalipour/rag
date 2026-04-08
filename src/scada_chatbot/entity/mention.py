import hashlib
from scada_chatbot.entity.__types__ import Entity, Mention, MentionRelationship


def stringify_mention(mention: Mention) -> str:
    return f"{mention['location']}:{mention['position']}"


def parse_mention(mention_string: str) -> Mention:
    location, position = mention_string.split(":")
    return {
        "location": location,
        "position": int(position),
    }


def hash_mentions(mentions: list[Mention]) -> str:
    data = "|".join(map(stringify_mention, mentions)).encode()
    return hashlib.sha256(data).hexdigest()


def derive_mention_relationships(
    entity: Entity,
) -> list[MentionRelationship]:
    return [
        {
            "source": appearance["location"],
            "target": entity["id"],
        }
        for appearance in entity["appearances"]
    ]
