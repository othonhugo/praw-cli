from __future__ import annotations

from prawler.cli.options import FieldsOption, FilterOption, FormatOption, LimitOption, OutputOption, SortOption, UserMode, UserModeOption, UsernameArg
from prawler.client import RedditPrawClient
from prawler.config import get_config
from prawler.crawler import CommentCrawler, PostCrawler, RedditorCrawler, RedditorProfileConfig, SubredditSort, UserCommentConfig, UserCrawlConfig
from prawler.output import get_formatter, make_sink
from prawler.pipeline import build_pipeline, make_field_select_stage, make_filter_stage


def user(
    username: UsernameArg,
    mode: UserModeOption = UserMode.POSTS,
    sort: SortOption = "new",
    limit: LimitOption = 100,
    format: FormatOption = "jsonl",
    output: OutputOption = "-",
    fields: FieldsOption = None,
    filter: FilterOption = None,
) -> None:
    """Crawl a Redditor's posts, comments, or profile."""

    cfg = get_config()
    client = RedditPrawClient.from_config(cfg)

    match mode:
        case UserMode.POSTS:
            stream = PostCrawler(client).from_user(UserCrawlConfig(username, SubredditSort(sort), limit))
            records = (item.to_dict() for item in stream)

        case UserMode.COMMENTS:
            stream = CommentCrawler(client).from_user(UserCommentConfig(username, sort, limit))
            records = (item.to_dict() for item in stream)

        case UserMode.PROFILE:
            stream = RedditorCrawler(client).from_usernames(RedditorProfileConfig([username]))
            records = (item.to_dict() for item in stream)

    pipeline = build_pipeline(
        *[make_filter_stage(f) for f in (filter or [])],
        make_field_select_stage(fields.split(",") if fields else None),
    )

    make_sink(output).write(get_formatter(format).format(pipeline(records)))
