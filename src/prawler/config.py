from __future__ import annotations

import os


class Config:
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    reddit_username: str | None
    reddit_password: str | None

    def __init__(self) -> None:
        self.reddit_client_id = self._require("PRAWLER_CLIENT_ID")
        self.reddit_client_secret = self._require("PRAWLER_CLIENT_SECRET")
        self.reddit_user_agent = os.getenv("PRAWLER_USER_AGENT", "prawler/0.2")
        self.reddit_username = os.getenv("PRAWLER_USERNAME")
        self.reddit_password = os.getenv("PRAWLER_PASSWORD")

    @staticmethod
    def _require(key: str) -> str:
        value = os.getenv(key)

        if not value:
            raise SystemExit(f"Missing required environment variable: {key}")

        return value


def get_config() -> Config:
    return Config()
