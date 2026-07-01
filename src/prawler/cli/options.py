from __future__ import annotations

from enum import StrEnum
from typing import Annotated

import typer

from prawler.crawler import SearchSort, SubredditSort, TimeFilter

# Arguments

SubredditArg = Annotated[
    str,
    typer.Argument(help="Subreddit name (without r/)."),
]

QueryArg = Annotated[
    str,
    typer.Argument(help="Search query string."),
]

UsernameArg = Annotated[
    str,
    typer.Argument(help="Reddit username (without u/)."),
]

SourceArg = Annotated[
    str,
    typer.Argument(help="Submission URL/ID or username (prefix with u/ for user)."),
]

# Shared options

FormatOption = Annotated[
    str,
    typer.Option("--format", "-f", help="Output format: json | jsonl | csv | table | markdown."),
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

FilterOption = Annotated[
    list[str] | None,
    typer.Option("--filter", "-F", help="Filter expression (repeatable)."),
]

TimeFilterOption = Annotated[
    TimeFilter,
    typer.Option("--time", "-t", help="Time window (top/controversial only)."),
]

SortOption = Annotated[
    str,
    typer.Option("--sort", "-s", help="Sort order."),
]

# Command-specific options

SubredditSortOption = Annotated[
    SubredditSort,
    typer.Option("--sort", "-s", help="Sort order."),
]

SearchSortOption = Annotated[
    SearchSort,
    typer.Option("--sort", "-s", help="Sort order."),
]

SubredditOption = Annotated[
    str,
    typer.Option("--sub", help="Subreddit to search within."),
]


class UserMode(StrEnum):
    POSTS = "posts"
    COMMENTS = "comments"
    PROFILE = "profile"


UserModeOption = Annotated[
    UserMode,
    typer.Option("--mode", help="What to fetch: posts | comments | profile."),
]
