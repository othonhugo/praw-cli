from __future__ import annotations

import csv
import io
import json
from typing import Iterator


class JsonFormatter:
    def format(self, items: Iterator[dict]) -> Iterator[str]:
        yield json.dumps(list(items), ensure_ascii=False, indent=2) + "\n"


class JsonLFormatter:
    def format(self, items: Iterator[dict]) -> Iterator[str]:
        for item in items:
            yield json.dumps(item, ensure_ascii=False) + "\n"


class CsvFormatter:
    def format(self, items: Iterator[dict]) -> Iterator[str]:
        rows = list(items)

        if not rows:
            return

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

        yield buf.getvalue()


class MarkdownFormatter:
    def format(self, items: Iterator[dict]) -> Iterator[str]:
        rows = list(items)

        if not rows:
            return

        headers = list(rows[0].keys())
        sep = " | ".join("---" for _ in headers)

        yield "| " + " | ".join(headers) + " |\n"
        yield "| " + sep + " |\n"

        for row in rows:
            cells = " | ".join(str(row.get(h, "")) for h in headers)
            yield "| " + cells + " |\n"


class TableFormatter:
    def format(self, items: Iterator[dict]) -> Iterator[str]:
        try:
            from rich.console import Console
            from rich.table import Table
        except ImportError:
            raise SystemExit("Install rich for table output: uv add rich")

        rows = list(items)

        if not rows:
            return

        table = Table()

        for col in rows[0].keys():
            table.add_column(col)

        for row in rows:
            table.add_row(*[str(v) for v in row.values()])

        buf = io.StringIO()
        Console(file=buf, highlight=False).print(table)
        yield buf.getvalue()
