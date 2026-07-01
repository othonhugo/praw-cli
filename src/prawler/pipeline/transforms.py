from __future__ import annotations

from collections.abc import Iterator

from prawler.pipeline.stage import PipelineStage


def make_field_select_stage(fields: list[str] | None) -> PipelineStage:
    if not fields:
        return lambda stream: stream

    def stage(stream: Iterator[dict]) -> Iterator[dict]:
        return ({k: record[k] for k in fields if k in record} for record in stream)

    return stage
