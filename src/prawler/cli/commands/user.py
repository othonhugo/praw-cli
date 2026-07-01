from __future__ import annotations

from enum import StrEnum

import typer

from prawler.cli.options import FieldsOption, FormatOption, LimitOption, OutputOption
from prawler.client import RedditPrawClient
from prawler.config import get_config
from prawler.crawler import (
    CommentCrawler,
    PostCrawler,
    RedditorCrawler,
    RedditorProfileConfig,
    UserCommentConfig,
    UserCrawlConfig,
)
from prawler.output import get_formatter, make_sink

app = typer.Typer()


class UserMode(StrEnum):
    POSTS = "posts"
    COMMENTS = "comments"
    PROFILE = "profile"


@app.command()
def user(
    username: str = typer.Argument(help="Reddit username (without u/)."),
    mode: UserMode = typer.Option(UserMode.POSTS, help="What to fetch: posts | comments | profile."),
    sort: str = typer.Option("new", help="Sort order (posts/comments only)."),
    limit: LimitOption = 100,
    format: FormatOption = "jsonl",
    output: OutputOption = "-",
    fields: FieldsOption = None,
) -> None:
    cfg = get_config()
    client = RedditPrawClient.from_config(cfg)
    field_list = fields.split(",") if fields else None

    match mode:
        case UserMode.POSTS:
            from prawler.crawler import SubredditSort

            post_stream = PostCrawler(client).from_user(UserCrawlConfig(username, SubredditSort(sort), limit))
            records = (post.to_dict(field_list) for post in post_stream)

        case UserMode.COMMENTS:
            comment_stream = CommentCrawler(client).from_user(UserCommentConfig(username, sort, limit))
            records = (comment.to_dict(field_list) for comment in comment_stream)

        case UserMode.PROFILE:
            redditor_stream = RedditorCrawler(client).from_usernames(RedditorProfileConfig([username]))
            records = (redditor.to_dict(field_list) for redditor in redditor_stream)

    make_sink(output).write(get_formatter(format).format(records))
