from __future__ import annotations

import typer

from prawler.cli.options import FieldsOption, FormatOption, LimitOption, OutputOption
from prawler.client import RedditPrawClient
from prawler.config import get_config
from prawler.crawler import PostCrawler, SubredditCrawlConfig, SubredditSort, TimeFilter
from prawler.output import get_formatter, make_sink

app = typer.Typer()


@app.command()
def posts(
    subreddit: str = typer.Argument(help="Subreddit name (without r/)."),
    sort: SubredditSort = typer.Option(SubredditSort.HOT, help="Sort order."),
    time_filter: TimeFilter = typer.Option(TimeFilter.ALL, help="Time window (top/controversial only)."),
    limit: LimitOption = 100,
    format: FormatOption = "jsonl",
    output: OutputOption = "-",
    fields: FieldsOption = None,
) -> None:
    cfg = get_config()
    client = RedditPrawClient.from_config(cfg)
    crawler = PostCrawler(client)

    field_list = fields.split(",") if fields else None
    stream = crawler.from_subreddit(SubredditCrawlConfig(subreddit, sort, time_filter, limit))
    records = (post.to_dict(field_list) for post in stream)

    make_sink(output).write(get_formatter(format).format(records))
