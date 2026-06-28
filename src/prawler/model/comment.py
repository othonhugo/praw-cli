from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from praw.models import Comment as PrawComment


@dataclass(frozen=True)
class Comment:
    # Identity
    id: str
    permalink: str

    # Relationships
    submission_id: str
    submission_title: str
    subreddit: str
    author: str | None
    parent_id: str

    # Content
    body: str
    depth: int

    # Engagement
    score: int

    # Metadata
    created_utc: datetime
    is_submitter: bool
    stickied: bool
    locked: bool
    nsfw: bool
    edited: bool

    def to_dict(self, fields: list[str] | None = None) -> dict:
        data = asdict(self)
        data["created_utc"] = self.created_utc.isoformat()

        if fields:
            data = {k: data[k] for k in fields if k in data}

        return data

    @classmethod
    def from_praw(cls, comment: PrawComment) -> "Comment":
        return cls(
            id=comment.id,
            permalink=comment.permalink,
            submission_id=comment.submission.id,
            submission_title=comment.submission.title,
            subreddit=comment.subreddit.display_name,
            author=comment.author.name if comment.author else None,
            parent_id=comment.parent_id,
            body=comment.body or "",
            depth=comment.depth,
            score=comment.score,
            created_utc=datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
            is_submitter=comment.is_submitter,
            stickied=comment.stickied,
            locked=comment.locked,
            nsfw=comment.submission.over_18,
            edited=bool(comment.edited),
        )

    @property
    def age_days(self) -> float:
        delta = datetime.now(tz=timezone.utc) - self.created_utc

        return delta.total_seconds() / 86_400
