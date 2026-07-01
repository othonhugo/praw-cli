from __future__ import annotations

from collections.abc import Iterator, Callable
from functools import reduce

PipelineStage = Callable[[Iterator[dict]], Iterator[dict]]


def build_pipeline(*stages: PipelineStage) -> PipelineStage:
    if not stages:
        return lambda stream: stream

    return reduce(lambda f, g: lambda stream: g(f(stream)), stages)
