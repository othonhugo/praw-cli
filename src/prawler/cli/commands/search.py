from __future__ import annotations

import typer

from prawler.cli.options import FieldsOption, FormatOption, LimitOption, OutputOption
from prawler.client import RedditPrawClient
from prawler.config import get_config
from prawler.crawler import PostCrawler, SearchCrawlConfig, SearchSort, TimeFilter
from prawler.output import get_formatter, make_sink

app = typer.Typer()


@app.command()
def search(
    query: str = typer.Argument(help="Search query string."),
    subreddit: str = typer.Option("all", help="Subreddit to search within."),
    sort: SearchSort = typer.Option(SearchSort.RELEVANCE, help="Sort order."),
    time_filter: TimeFilter = typer.Option(TimeFilter.ALL, help="Time window."),
    limit: LimitOption = 100,
    format: FormatOption = "jsonl",
    output: OutputOption = "-",
    fields: FieldsOption = None,
) -> None:
    cfg = get_config()
    client = RedditPrawClient.from_config(cfg)
    crawler = PostCrawler(client)

    field_list = fields.split(",") if fields else None
    stream = crawler.from_search(SearchCrawlConfig(query, subreddit, sort, time_filter, limit))
    records = (post.to_dict(field_list) for post in stream)

    make_sink(output).write(get_formatter(format).format(records))
