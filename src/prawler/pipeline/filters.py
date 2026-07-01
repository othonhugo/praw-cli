from __future__ import annotations

import re
from collections.abc import Iterator

from prawler.pipeline.stage import PipelineStage

OPERATORS = ["~=", "!=", ">=", "<=", " in ", ">", "<", "="]


def _parse(expr: str) -> tuple[str, str, str]:
    for op in OPERATORS:
        idx = expr.find(op)
        if idx != -1:
            field = expr[:idx].strip()
            value = expr[idx + len(op) :].strip()
            return field, op.strip(), value

    raise ValueError(f"Invalid filter expression: {expr}")


def _coerce(value: str):
    if value.lower() in ("true", "false"):
        return value.lower() == "true"

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def _make_predicate(field: str, op: str, raw_value: str):
    match op:
        case "=":
            target = _coerce(raw_value)
            return lambda r: _coerce(str(r.get(field, ""))) == target

        case "!=":
            target = _coerce(raw_value)
            return lambda r: _coerce(str(r.get(field, ""))) != target

        case ">=" | "<=" | ">" | "<":
            target = _coerce(raw_value)
            ops = {">=": float.__ge__, "<=": float.__le__, ">": float.__gt__, "<": float.__lt__}
            cmp = ops[op]
            return lambda r: cmp(float(r.get(field, 0)), float(target))

        case "~=":
            pattern = re.compile(raw_value, re.IGNORECASE)
            return lambda r: bool(pattern.search(str(r.get(field, ""))))

        case "in":
            values = {v.strip() for v in raw_value.split(",")}
            return lambda r: str(r.get(field, "")) in values

        case _:
            raise ValueError(f"Unknown operator: {op}")


def make_filter_stage(expr: str) -> PipelineStage:
    field, op, value = _parse(expr)
    predicate = _make_predicate(field, op, value)

    def stage(stream: Iterator[dict]) -> Iterator[dict]:
        return (record for record in stream if predicate(record))

    return stage
