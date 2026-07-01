from __future__ import annotations

from prawler.cli.options import FieldsOption, FilterOption, FormatOption, LimitOption, OutputOption, QueryArg, SearchSortOption, SubredditOption, TimeFilterOption
from prawler.client import RedditPrawClient
from prawler.config import get_config
from prawler.crawler import PostCrawler, SearchCrawlConfig, SearchSort, TimeFilter
from prawler.output import get_formatter, make_sink
from prawler.pipeline import build_pipeline, make_field_select_stage, make_filter_stage


def search(
    query: QueryArg,
    subreddit: SubredditOption = "all",
    sort: SearchSortOption = SearchSort.RELEVANCE,
    time_filter: TimeFilterOption = TimeFilter.ALL,
    limit: LimitOption = 100,
    format: FormatOption = "jsonl",
    output: OutputOption = "-",
    fields: FieldsOption = None,
    filter: FilterOption = None,
) -> None:
    """Search Reddit posts."""

    cfg = get_config()
    client = RedditPrawClient.from_config(cfg)
    stream = PostCrawler(client).from_search(SearchCrawlConfig(query, subreddit, sort, time_filter, limit))
    records = (post.to_dict() for post in stream)

    pipeline = build_pipeline(
        *[make_filter_stage(f) for f in (filter or [])],
        make_field_select_stage(fields.split(",") if fields else None),
    )

    make_sink(output).write(get_formatter(format).format(pipeline(records)))
