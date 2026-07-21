from __future__ import annotations

import itertools
import time
from collections.abc import Iterator

from prawler.output import OutputFormat
from prawler.cli.options import FieldsOption, FilterOption, FormatOption, LimitOption, OutputOption, SortOption, SourceArg
from prawler.client import RedditPrawClient
from prawler.config import get_config
from prawler.crawler import CommentCrawler, SubmissionCommentConfig, UserCommentConfig
from prawler.output import get_formatter, make_sink
from prawler.pipeline import build_pipeline, make_field_select_stage, make_filter_stage

COMMENTS_MAX_SECONDS = 300


def _with_deadline(records: Iterator[dict[str, object]], max_seconds: int) -> Iterator[dict[str, object]]:
    deadline = time.monotonic() + max_seconds

    for record in records:
        if time.monotonic() >= deadline:
            return

        yield record


def comments(
    source: SourceArg,
    sort: SortOption = "new",
    limit: LimitOption = 100,
    format: FormatOption = OutputFormat.JSONL,
    output: OutputOption = "-",
    fields: FieldsOption = None,
    filter: FilterOption = None,
) -> None:
    """Crawl comments from a submission (URL or ID) or a user (u/username)."""

    cfg = get_config()
    client = RedditPrawClient.from_config(cfg)
    crawler = CommentCrawler(client)

    if source.startswith("u/"):
        username = source.removeprefix("u/")
        stream = crawler.from_user(UserCommentConfig(username, sort, None))
    elif source.startswith("http"):
        stream = crawler.from_submission(SubmissionCommentConfig(submission_url=source, limit=None))
    else:
        stream = crawler.from_submission(SubmissionCommentConfig(submission_id=source, limit=None))

    records = (comment.to_dict() for comment in stream)

    pipeline = build_pipeline(
        *[make_filter_stage(f) for f in (filter or [])],
        make_field_select_stage(fields.split(",") if fields else None),
    )

    filtered_records = _with_deadline(pipeline(records), COMMENTS_MAX_SECONDS)

    if limit is not None:
        filtered_records = itertools.islice(filtered_records, limit)

    make_sink(output).write(get_formatter(format).format(filtered_records))
