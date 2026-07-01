from .comments import app as comments_app
from .posts import app as posts_app
from .search import app as search_app
from .user import app as user_app

__all__ = [
    "comments_app",
    "posts_app",
    "search_app",
    "user_app",
]
