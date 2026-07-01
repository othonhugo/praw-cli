from dataclasses import dataclass
from typing import Iterator

import praw.models

from prawler.client import RedditPrawClient
from prawler.model import Comment


@dataclass(frozen=True)
class SubmissionCommentConfig:
    submission_id: str | None = None
    submission_url: str | None = None
    limit: int | None = None


@dataclass(frozen=True)
class UserCommentConfig:
    username: str
    sort: str = "new"
    limit: int | None = 100


class CommentCrawler:
    def __init__(self, client: RedditPrawClient) -> None:
        self._client = client

    def from_submission(self, cfg: SubmissionCommentConfig) -> Iterator[Comment]:
        submission = self._client.submission(
            url=cfg.submission_url,
            id=cfg.submission_id,
        )

        submission.comments.replace_more(limit=cfg.limit)

        yield from self._map(submission.comments.list())

    def from_user(self, cfg: UserCommentConfig) -> Iterator[Comment]:
        redditor = self._client.redditor(cfg.username)

        match cfg.sort:
            case "hot":
                comments = redditor.comments.hot(limit=cfg.limit)
            case "top":
                comments = redditor.comments.top(limit=cfg.limit)
            case "controversial":
                comments = redditor.comments.controversial(limit=cfg.limit)
            case _:
                comments = redditor.comments.new(limit=cfg.limit)

        yield from self._map(
            item for item in comments if isinstance(item, praw.models.Comment)
        )

    def _map(self, comments) -> Iterator[Comment]:
        for comment in comments:
            try:
                yield Comment.from_praw(comment)
            except Exception:  # noqa: BLE001
                pass
