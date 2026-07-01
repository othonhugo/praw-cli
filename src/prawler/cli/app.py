from __future__ import annotations

import typer

from prawler.cli.commands import comments, posts, search, user

app = typer.Typer(
    name="prawler",
    help="Composable Reddit crawler. Fetch posts, comments, and user data.",
    no_args_is_help=True,
)

app.command()(posts)
app.command()(comments)
app.command()(search)
app.command()(user)
