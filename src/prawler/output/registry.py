from __future__ import annotations

from .formatters import CsvFormatter, JsonFormatter, JsonLFormatter, MarkdownFormatter, TableFormatter

FORMATTERS: dict[str, type] = {
    "json": JsonFormatter,
    "jsonl": JsonLFormatter,
    "csv": CsvFormatter,
    "table": TableFormatter,
    "markdown": MarkdownFormatter,
}


def get_formatter(name: str):
    cls = FORMATTERS.get(name)

    if cls is None:
        valid = ", ".join(FORMATTERS)
        raise SystemExit(f"Unknown format '{name}'. Valid options: {valid}")

    return cls()
