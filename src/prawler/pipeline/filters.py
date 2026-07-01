from __future__ import annotations

import re
from collections.abc import Callable, Iterator

from prawler.pipeline.stage import PipelineStage, Record

OPERATORS = [
    " starts_with ",
    " ends_with ",
    " has_all ",
    " len>= ",
    " len<= ",
    " len> ",
    " len< ",
    " len= ",
    " has ",
    " in ",
    "~=",
    "!=",
    ">=",
    "<=",
    ">",
    "<",
    "=",
]

Predicate = Callable[[Record], bool]


def _parse(expr: str) -> tuple[str, str, str]:
    for op in OPERATORS:
        idx = expr.find(op)

        if idx != -1:
            field = expr[:idx].strip()
            value = expr[idx + len(op) :].strip()

            return field, op.strip(), value

    raise ValueError(f"Invalid filter expression: {expr}")


def _coerce(value: str) -> bool | int | float | str:
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


def _make_predicate(field: str, op: str, raw_value: str) -> Predicate:
    match op:
        case "=":
            target = _coerce(raw_value)
            return lambda r: _coerce(str(r.get(field, ""))) == target

        case "!=":
            target = _coerce(raw_value)
            return lambda r: _coerce(str(r.get(field, ""))) != target

        case ">=" | "<=" | ">" | "<":
            target = _coerce(raw_value)

            ops_float = {">=": float.__ge__, "<=": float.__le__, ">": float.__gt__, "<": float.__lt__}
            ops_str = {">=": str.__ge__, "<=": str.__le__, ">": str.__gt__, "<": str.__lt__}

            def _cmp(val: object, tgt: object) -> bool:
                if isinstance(tgt, (int, float)):
                    try:
                        return ops_float[op](float(str(val)), float(tgt))
                    except (ValueError, TypeError):
                        pass

                return ops_str[op](str(val), str(tgt))

            return lambda r: _cmp(r.get(field, ""), target)

        case "len>=" | "len<=" | "len>" | "len<" | "len=":
            target_len = int(raw_value)

            ops_len = {"len>=": int.__ge__, "len<=": int.__le__, "len>": int.__gt__, "len<": int.__lt__, "len=": int.__eq__}
            cmp_len = ops_len[op]

            return lambda r: cmp_len(len(str(r.get(field, ""))), target_len)

        case "starts_with":
            return lambda r: str(r.get(field, "")).startswith(raw_value)

        case "ends_with":
            return lambda r: str(r.get(field, "")).endswith(raw_value)

        case "~=":
            pattern = re.compile(raw_value, re.IGNORECASE)

            return lambda r: bool(pattern.search(str(r.get(field, ""))))

        case "in":
            values = {v.strip() for v in raw_value.split(",")}

            return lambda r: str(r.get(field, "")) in values

        case "has":
            keywords_any = [v.strip().lower() for v in raw_value.split(",")]

            return lambda r: any(k in str(r.get(field, "")).lower() for k in keywords_any)

        case "has_all":
            keywords_all = [v.strip().lower() for v in raw_value.split(",")]

            return lambda r: all(k in str(r.get(field, "")).lower() for k in keywords_all)

        case _:
            raise ValueError(f"Unknown operator: {op}")


def make_filter_stage(expr: str) -> PipelineStage:
    field, op, value = _parse(expr)
    predicate = _make_predicate(field, op, value)

    def stage(stream: Iterator[Record]) -> Iterator[Record]:
        return (record for record in stream if predicate(record))

    return stage
