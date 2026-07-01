from dataclasses import dataclass
from enum import StrEnum
from typing import Iterator

from praw.models import Submission

from prawler.client import RedditPrawClient
from prawler.model import Post


class SubredditSort(StrEnum):
    HOT = "hot"
    NEW = "new"
    TOP = "top"
    RISING = "rising"
    CONTROVERTIAL = "controversial"


class SearchSort(StrEnum):
    RELEVANCE = "relevance"
    HOT = "hot"
    TOP = "top"
    NEW = "new"
    COMMENTS = "comments"


class TimeFilter(StrEnum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    ALL = "all"


@dataclass(frozen=True)
class SubredditCrawlConfig:
    subreddit: str
    sort: SubredditSort = SubredditSort.HOT
    time_filter: TimeFilter = TimeFilter.ALL
    limit: int | None = 100


@dataclass(frozen=True)
class SearchCrawlConfig:
    query: str
    subreddit: str = "all"
    sort: SearchSort = SearchSort.RELEVANCE
    time_filter: TimeFilter = TimeFilter.ALL
    limit: int | None = 100


@dataclass(frozen=True)
class UserCrawlConfig:
    username: str
    sort: SubredditSort = SubredditSort.NEW
    limit: int | None = 100


@dataclass(frozen=True)
class UrlCrawlConfig:
    url: str


class PostCrawler:
    def __init__(self, client: RedditPrawClient) -> None:
        self._client = client

    def from_subreddit(self, cfg: SubredditCrawlConfig) -> Iterator[Post]:
        sub = self._client.subreddit(cfg.subreddit)

        match cfg.sort:
            case SubredditSort.HOT:
                submissions = sub.hot(limit=cfg.limit)
            case SubredditSort.NEW:
                submissions = sub.new(limit=cfg.limit)
            case SubredditSort.TOP:
                submissions = sub.top(limit=cfg.limit, time_filter=cfg.time_filter.value)
            case SubredditSort.RISING:
                submissions = sub.rising(limit=cfg.limit)
            case SubredditSort.CONTROVERTIAL:
                submissions = sub.controversial(limit=cfg.limit, time_filter=cfg.time_filter.value)

        yield from self._map(submissions)

    def from_search(self, cfg: SearchCrawlConfig) -> Iterator[Post]:
        sub = self._client.subreddit(cfg.subreddit)

        results = sub.search(
            query=cfg.query,
            sort=cfg.sort.value,
            time_filter=cfg.time_filter.value,
            limit=cfg.limit,
        )

        yield from self._map(results)

    def from_user(self, cfg: UserCrawlConfig) -> Iterator[Post]:
        redditor = self._client.redditor(cfg.username)

        match cfg.sort:
            case SubredditSort.HOT:
                submissions = redditor.hot()
            case SubredditSort.NEW:
                submissions = redditor.new()
            case SubredditSort.TOP:
                submissions = redditor.top()
            case SubredditSort.RISING:
                submissions = redditor.hot()
            case SubredditSort.CONTROVERTIAL:
                submissions = redditor.hot()

        yield from self._map(item for item in submissions if isinstance(item, Submission))

    def from_url(self, cfg: UrlCrawlConfig) -> Iterator[Post]:
        submission = self._client.submission(url=cfg.url)

        yield Post.from_submission(submission)

    def _map(self, submissions: Iterator[Submission]) -> Iterator[Post]:
        for sub in submissions:
            try:
                yield Post.from_submission(sub)
            except Exception:  # noqa: BLE001
                pass
