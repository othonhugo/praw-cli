from __future__ import annotations

import typer

from prawler.cli.commands import comments_app, posts_app, search_app, user_app

app = typer.Typer(
    name="prawler",
    help="Composable Reddit crawler. Fetch posts, comments, and user data.",
    no_args_is_help=True,
)

app.add_typer(posts_app, name="posts")
app.add_typer(comments_app, name="comments")
app.add_typer(search_app, name="search")
app.add_typer(user_app, name="user")
