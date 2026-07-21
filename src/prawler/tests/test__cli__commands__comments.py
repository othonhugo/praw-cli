from __future__ import annotations

from importlib import import_module
from types import SimpleNamespace

comments_module = import_module("prawler.cli.commands.comments")


class FakeComment:
    def __init__(self, body: str) -> None:
        self._body = body

    def to_dict(self) -> dict[str, str]:
        return {"body": self._body}


class FakeCrawler:
    def __init__(self, stream: list[FakeComment]) -> None:
        self.stream = stream
        self.submission_limits: list[int | None] = []
        self.user_limits: list[int | None] = []

    def from_submission(self, cfg: object):
        self.submission_limits.append(getattr(cfg, "limit"))
        return iter(self.stream)

    def from_user(self, cfg: object):
        self.user_limits.append(getattr(cfg, "limit"))
        return iter(self.stream)


class FakeFormatter:
    def format(self, records):
        return records


class FakeSink:
    def __init__(self) -> None:
        self.records: list[dict[str, str]] = []

    def write(self, records) -> None:
        self.records = list(records)


def test_comments_limit_applies_after_filter(monkeypatch) -> None:
    crawler = FakeCrawler(
        [
            FakeComment("reject-1"),
            FakeComment("keep-1"),
            FakeComment("keep-2"),
            FakeComment("keep-3"),
        ]
    )
    sink = FakeSink()

    monkeypatch.setattr(comments_module, "get_config", lambda: SimpleNamespace())
    monkeypatch.setattr(comments_module.RedditPrawClient, "from_config", lambda cfg: SimpleNamespace())
    monkeypatch.setattr(comments_module, "CommentCrawler", lambda client: crawler)
    monkeypatch.setattr(comments_module, "get_formatter", lambda fmt: FakeFormatter())
    monkeypatch.setattr(comments_module, "make_sink", lambda output: sink)

    comments_module.comments(
        source="xyz123",
        limit=2,
        filter=["body ~= keep"],
    )

    assert crawler.submission_limits == [None]
    assert [record["body"] for record in sink.records] == ["keep-1", "keep-2"]


def test_comments_user_source_is_unbounded(monkeypatch) -> None:
    crawler = FakeCrawler([FakeComment("keep-1")])
    sink = FakeSink()

    monkeypatch.setattr(comments_module, "get_config", lambda: SimpleNamespace())
    monkeypatch.setattr(comments_module.RedditPrawClient, "from_config", lambda cfg: SimpleNamespace())
    monkeypatch.setattr(comments_module, "CommentCrawler", lambda client: crawler)
    monkeypatch.setattr(comments_module, "get_formatter", lambda fmt: FakeFormatter())
    monkeypatch.setattr(comments_module, "make_sink", lambda output: sink)

    comments_module.comments(
        source="u/tester",
        limit=1,
    )

    assert crawler.user_limits == [None]
    assert [record["body"] for record in sink.records] == ["keep-1"]