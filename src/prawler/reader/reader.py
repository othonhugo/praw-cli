from __future__ import annotations

import csv
import io
import json
import sys
from collections.abc import Iterator
from enum import StrEnum
from pathlib import Path

from prawler.pipeline.stage import Record

_STDIN_SENTINEL = "-"

_EXTENSION_MAP: dict[str, str] = {
    ".jsonl": "jsonl",
    ".ndjson": "jsonl",
    ".json": "json",
    ".csv": "csv",
}


class FileFormat(StrEnum):
    JSONL = "jsonl"
    JSON = "json"
    CSV = "csv"


class FileReader:
    """Read records from a local file or stdin, yielding Record dicts.

    Supported sources:
    - A file path ending in .jsonl / .ndjson / .json / .csv
    - The special string "-" to read from stdin

    The format can be provided explicitly via *fmt*. When *fmt* is ``None``
    the format is auto-detected from the file extension. Stdin always
    requires an explicit format (defaults to JSONL when not provided).
    """

    def read(self, source: str | Path, fmt: FileFormat | None = None) -> Iterator[Record]:
        is_stdin = str(source) == _STDIN_SENTINEL
        resolved_fmt = fmt or self._detect_format(source, is_stdin)

        if is_stdin:
            yield from self._parse(sys.stdin, resolved_fmt, name="<stdin>")
        else:
            path = Path(source)

            if not path.exists():
                raise FileNotFoundError(f"Input file not found: {path}")
            with path.open(encoding="utf-8") as fh:
                yield from self._parse(fh, resolved_fmt, name=str(path))

    def _detect_format(self, source: str | Path, is_stdin: bool) -> FileFormat:
        if is_stdin:
            return FileFormat.JSONL

        ext = Path(source).suffix.lower()
        name = _EXTENSION_MAP.get(ext)

        if name is None:
            raise ValueError(f"Cannot auto-detect input format from extension '{ext}'. Use --input-format to specify it explicitly.")

        return FileFormat(name)

    def _parse(self, fh: io.TextIOBase, fmt: FileFormat, name: str) -> Iterator[Record]:
        match fmt:
            case FileFormat.JSONL:
                yield from self._parse_jsonl(fh)
            case FileFormat.JSON:
                yield from self._parse_json(fh, name)
            case FileFormat.CSV:
                yield from self._parse_csv(fh)

    @staticmethod
    def _parse_jsonl(fh: io.TextIOBase) -> Iterator[Record]:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {lineno}: {exc}") from exc

            if not isinstance(obj, dict):
                raise TypeError(f"Expected a JSON object on line {lineno}, got {type(obj).__name__}")

            yield obj  # type: ignore[misc]

    @staticmethod
    def _parse_json(fh: io.TextIOBase, name: str) -> Iterator[Record]:
        try:
            data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {name}: {exc}") from exc

        if not isinstance(data, list):
            raise TypeError(f"Expected a JSON array in {name}, got {type(data).__name__}")

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise TypeError(f"Expected a JSON object at index {idx}, got {type(item).__name__}")

            yield item  # type: ignore[misc]

    @staticmethod
    def _parse_csv(fh: io.TextIOBase) -> Iterator[Record]:
        reader = csv.DictReader(fh)

        for row in reader:
            yield dict(row)  # type: ignore[misc]
