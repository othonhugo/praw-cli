# Architectural Decision Records (ADRs)

This document tracks important architectural decisions made during the development of Prawler.

## ADR-001 — Use Typer over Click or argparse

**Context:** The CLI needs sub-commands, shared options, and auto-generated `--help`.

**Decision:** Use Typer. It provides Click's composability through Python type annotations, eliminating decorator-heavy option definitions. `typer[all]` adds `rich` integration for help formatting.

**Trade-offs:** Typer adds an indirect dependency on Click. Acceptable given it is a stable, well-maintained wrapper.

## ADR-002 — Lazy iterators throughout the pipeline

**Context:** Crawls may yield thousands of posts. Storing them in a list before filtering is wasteful.

**Decision:** Every stage — crawler, pipeline, formatter, sink — consumes and produces `Iterator[T]`. The sink's `write()` loop is the only place that "drives" the pipeline.

**Trade-offs:** Lazy iterators cannot be rewound. Any stage that needs to look ahead (e.g. sorting by score) must buffer internally and document this explicitly.

## ADR-003 — PRAW stays behind the client package boundary

**Context:** `praw.models.Submission` is a PRAW-specific type with lazy attribute loading. Leaking it into the pipeline would couple every stage to PRAW's internals.

**Decision:** `_to_post()` / `_to_comment()` are the only methods that access PRAW attributes. All downstream code receives frozen Python dataclasses.

**Trade-offs:** Adds one mapping step. Benefit: replacing PRAW requires changes only in `client/` and `crawler/`.

## ADR-004 — Formatter and Sink are Protocols, not ABCs

**Context:** Python's `Protocol` enables structural subtyping. Any class with the right methods satisfies the interface without explicit inheritance.

**Decision:** `Formatter` and `Sink` are `typing.Protocol`. Implementations do not inherit from a base class.

**Trade-offs:** Static analysis (mypy/pyright) is required to catch violations — runtime duck-typing errors are deferred to call time. This is the standard trade-off with structural typing and is acceptable for a CLI tool.

## ADR-005 — Config objects per crawl mode

**Context:** `PostCrawler` supports four distinct crawl modes (subreddit, search, user, URL), each with different valid parameters.

**Decision:** Each mode has a dedicated frozen dataclass (`SubredditCrawlConfig`, `SearchCrawlConfig`, etc.) rather than a single method with many optional parameters.

**Trade-offs:** More types to maintain. Benefit: invalid combinations (e.g. `time_filter` on a user crawl) are impossible to construct, not caught at runtime.
