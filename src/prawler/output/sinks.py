from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterator


class StdoutSink:
    def write(self, chunks: Iterator[str]) -> None:
        for chunk in chunks:
            sys.stdout.write(chunk)


class FileSink:
    def __init__(self, path: Path) -> None:
        self._path = path

    def write(self, chunks: Iterator[str]) -> None:
        with self._path.open("w", encoding="utf-8") as fh:
            for chunk in chunks:
                fh.write(chunk)


class MultiSink:
    def __init__(self, sinks: list) -> None:
        self._sinks = sinks

    def write(self, chunks: Iterator[str]) -> None:
        collected = list(chunks)

        for sink in self._sinks:
            sink.write(iter(collected))


def make_sink(output: str):
    if output == "-":
        return StdoutSink()

    return FileSink(Path(output))
