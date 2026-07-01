from __future__ import annotations

from typing import Iterator, Protocol, runtime_checkable


@runtime_checkable
class Formatter(Protocol):
    def format(self, items: Iterator[dict]) -> Iterator[str]: ...


@runtime_checkable
class Sink(Protocol):
    def write(self, chunks: Iterator[str]) -> None: ...
