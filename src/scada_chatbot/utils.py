from ast import TypeVar
from typing import Iterator, Never, TypeVar


class UnreachableError(Exception):
    def __init__(self, value: Never):
        super().__init__(f"Unreachable type: {value}")


A = TypeVar("A")


def group(items: list[A], batch_size: int) -> Iterator[list[A]]:
    for index in range(0, len(items), batch_size):
        yield items[index : index + batch_size]
