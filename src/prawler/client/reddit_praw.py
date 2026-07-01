from __future__ import annotations

import praw
import praw.models
from tenacity import retry, stop_after_attempt, wait_exponential

from prawler.config import Config


class RedditPrawClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        if username and password:
            self._reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password,
            )
            self._reddit.read_only = False
        else:
            self._reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
            )
            self._reddit.read_only = True

    def subreddit(self, name: str) -> praw.models.Subreddit:
        return self._reddit.subreddit(name)

    def redditor(self, name: str) -> praw.models.Redditor:
        return self._reddit.redditor(name)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )
    def submission(self, *, url: str | None = None, id: str | None = None) -> praw.models.Submission:
        if url:
            return self._reddit.submission(url=url)

        if id:
            return self._reddit.submission(id=id)

        raise ValueError("provide url or id")

    @classmethod
    def from_config(cls, cfg: Config) -> "RedditPrawClient":
        return cls(
            client_id=cfg.reddit_client_id,
            client_secret=cfg.reddit_client_secret,
            user_agent=cfg.reddit_user_agent,
            username=cfg.reddit_username,
            password=cfg.reddit_password,
        )
