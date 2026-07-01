from __future__ import annotations

from typing import Annotated

import typer

FormatOption = Annotated[
    str,
    typer.Option("--format", "-f", help="Output format: json | jsonl | csv | table | markdown"),
]

OutputOption = Annotated[
    str,
    typer.Option("--output", "-o", help="Output destination. Use '-' for stdout."),
]

LimitOption = Annotated[
    int | None,
    typer.Option("--limit", "-n", help="Maximum number of items to fetch."),
]

FieldsOption = Annotated[
    str | None,
    typer.Option("--fields", help="Comma-separated list of fields to include."),
]
