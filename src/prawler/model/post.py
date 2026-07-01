from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from praw.models import Submission


@dataclass(frozen=True)
class Post:
    # Identity
    id: str
    title: str
    url: str
    permalink: str

    # Engagement
    score: int
    upvote_ratio: float
    num_comments: int

    # Metadata
    created_utc: datetime
    subreddit: str
    author: str | None
    selftext: str
    is_self: bool
    flair: str | None
    nsfw: bool
    spoiler: bool
    locked: bool
    stickied: bool
    domain: str

    def to_dict(self, fields: list[str] | None = None) -> dict:
        data = asdict(self)
        data["created_utc"] = self.created_utc.isoformat()

        if fields:
            data = {k: data[k] for k in fields if k in data}

        return data

    @classmethod
    def from_submission(cls, sub: Submission) -> "Post":
        return cls(
            id=sub.id,
            title=sub.title,
            url=sub.url,
            permalink=sub.permalink,
            score=sub.score,
            upvote_ratio=sub.upvote_ratio,
            num_comments=sub.num_comments,
            created_utc=datetime.fromtimestamp(sub.created_utc, tz=timezone.utc),
            subreddit=sub.subreddit.display_name,
            author=sub.author.name if sub.author else None,
            selftext=sub.selftext or "",
            is_self=sub.is_self,
            flair=sub.link_flair_text,
            nsfw=sub.over_18,
            spoiler=sub.spoiler,
            locked=sub.locked,
            stickied=sub.stickied,
            domain=sub.domain,
        )

    @property
    def age_days(self) -> float:
        delta = datetime.now(tz=timezone.utc) - self.created_utc

        return delta.total_seconds() / 86_400
