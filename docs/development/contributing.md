# Contributing and Development Guide

Thank you for your interest in contributing to Prawler! This guide covers the project setup and the common extension points.

## Project Structure

```
src/prawler/
├── __init__.py
├── __main__.py              # python -m prawler entrypoint
│
├── cli/
│   ├── app.py               # root Typer app, registers sub-commands
│   ├── options.py           # shared option type aliases
│   └── commands/
│       ├── posts.py
│       ├── comments.py
│       ├── search.py
│       └── user.py
│
├── client/
│   ├── reddit.py            # RedditClient (only praw importer)
│   └── rate_limiter.py
│
├── crawler/
│   ├── base.py              # BaseCrawler[T] abstract class
│   ├── post.py              # PostCrawler + *CrawlConfig dataclasses
│   └── comment.py           # CommentCrawler
│
├── pipeline/
│   ├── stage.py             # PipelineStage type + build_pipeline()
│   ├── filters.py           # FilterStage + --filter DSL parser
│   ├── transforms.py        # FieldSelectStage, FlattenStage
│   └── enrich.py            # EnrichStage (lazy user metadata)
│
├── output/
│   ├── base.py              # Formatter + Sink Protocols
│   ├── registry.py          # FORMATTERS dict
│   ├── sinks.py             # StdoutSink, FileSink, MultiSink, make_sink()
│   └── formatters/
│       ├── json_fmt.py
│       ├── jsonl_fmt.py     # preferred for streaming / large crawls
│       ├── csv_fmt.py
│       ├── table_fmt.py     # Rich-powered terminal table
│       └── markdown_fmt.py
│
├── model/
│   ├── post.py              # @dataclass(frozen=True) Post
│   └── comment.py           # @dataclass(frozen=True) Comment
│
└── config.py                # Config (pydantic-settings), get_config()

tests/
├── conftest.py              # shared fixtures, mock RedditClient factory
├── test_post_crawler.py
├── test_comment_crawler.py
├── test_pipeline_filters.py
├── test_pipeline_transforms.py
└── test_output_formatters.py
```

## Running the Code Locally

```bash
# install with dev dependencies
uv sync

# run the test suite
pytest

# lint and format
ruff check src/ tests/
ruff format src/ tests/

# type checking
mypy src/
```

## Extension Points

### Adding a new output format

1. Create `src/prawler/output/formatters/myformat_fmt.py` implementing `Formatter`.
2. Register it in `src/prawler/output/registry.py`:

```python
from prawler.output.formatters.myformat_fmt import MyFormatFormatter

FORMATTERS["myformat"] = MyFormatFormatter
```

Done. The CLI picks it up automatically via `--format myformat`.

### Adding a new pipeline stage

1. Create a function `make_my_stage(args) -> PipelineStage` in `pipeline/`.
2. Wire it in the command that needs it:

```python
stages.append(make_my_stage(args))
pipeline = build_pipeline(*stages)
```

### Adding a new crawl source

1. Create `src/prawler/crawler/mysource.py` with a class extending `BaseCrawler[T]`.
2. Add a new Typer sub-command in `cli/commands/`.
3. No changes required in the pipeline or output layers.
