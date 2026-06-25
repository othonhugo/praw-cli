# prawler

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-purple.svg)](https://github.com/astral-sh/ruff)

A composable Reddit crawler for the command line. Fetch posts and comments from any source, shape the data through a lazy filter pipeline, and emit it in any format — all without writing a single line of Python.

```bash
# stream the top 500 posts from r/MachineLearning as JSONL
prawler posts r/MachineLearning --sort top --time year --limit 500 --format jsonl

# search across r/programming, keep only high-signal posts, project to four fields
prawler search "New web framework" --sub r/programming \
  --filter "score>=100" --filter "num_comments>=10" \
  --fields id,title,score,url --format csv --output results.csv

# full comment tree of a submission, depth-first, minimum score 5
prawler comments https://reddit.com/r/Python/comments/xyz/ \
  --depth 10 --min-score 5 --format jsonl
```

## Contents

- [Features](#features)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Commands](#commands)
- [Filtering](#filtering)
- [Output formats](#output-formats)
- [Scientific use](#scientific-use)
- [Configuration](#configuration)
- [Development](#development)

## Features

- **Lazy pipeline** — the entire data path is `Iterator[T]`. A 100k-post crawl uses constant memory regardless of output size.
- **Composable filters** — chain `--filter` expressions using a concise DSL (`score>=100`, `flair~=Discussion`, `author!=AutoModerator`).
- **Flexible output** — JSONL, JSON, CSV, terminal table, or Markdown. Pair any format with stdout, a file, or multiple destinations simultaneously.
- **Reproducible datasets** — fixed random seeds, crawl manifests, config fingerprinting, and per-record provenance metadata for scientific use.
- **Resumable crawls** — checkpoint progress every N records; resume interrupted sessions without re-fetching from the start.
- **Zero business logic in the CLI** — every behaviour is controllable from `config.toml`, environment variables, or flags. No hardcoded limits.

## Installation

Requires Python 3.11 or later and a [Reddit API application](https://www.reddit.com/prefs/apps) (free, read-only access is sufficient for most use cases).

```bash
pip install ...
```

Or, to install from source:

```bash
git clone https://github.com/othonhugo/prawler
cd prawler
pip install -e ".[dev]"
```

### Credentials

Set your credentials once. Prawler reads them from environment variables, a config file, or both — they are never passed as positional arguments.

```bash
export PRAWLER_REDDIT_CLIENT_ID="your_client_id"
export PRAWLER_REDDIT_CLIENT_SECRET="your_client_secret"
export PRAWLER_REDDIT_USER_AGENT="prawler/0.1 by u/yourname"
```

Or write them to `~/.config/prawler/config.toml`:

```toml
[reddit]
client_id     = "your_client_id"
client_secret = "your_client_secret"
user_agent    = "prawler/0.1 by u/yourname"
```

## Quick start

```bash
# Subreddit listing — hot, new, top, rising, controversial
prawler posts r/python --sort new --limit 50

# Full-text search (r/all by default)
prawler search "asyncio tutorial" --sort relevance --time month

# All posts by a user
prawler posts --user spez --sort top --time all

# Single submission by URL
prawler posts https://reddit.com/r/Python/comments/abc123/

# Comment tree of a submission
prawler comments https://reddit.com/r/Python/comments/abc123/ --depth 5

# Pipe into jq, pandas, R — JSONL works everywhere
prawler posts r/datascience --format jsonl | jq '.score'
prawler posts r/datasets   --format csv   > datasets.csv
```

## Commands

### `prawler posts`

Fetch submissions from a subreddit, a user profile, or a direct URL.

```
Usage: prawler posts [OPTIONS] TARGET

Arguments:
  TARGET  Subreddit name (r/python or python) or a full submission URL.

Options:
  -u, --user TEXT            Fetch submissions by this username instead.
  -s, --sort [hot|new|top|rising|controversial]
                             Listing sort order.          [default: hot]
  -t, --time [hour|day|week|month|year|all]
                             Time window (top/controversial only).
                                                          [default: all]
  -f, --filter TEXT          Filter expression. Repeatable.
  -n, --limit INTEGER        Maximum records to fetch.   [default: 100]
      --fields TEXT          Comma-separated field projection.
      --format TEXT          Output format.              [default: jsonl]
  -o, --output TEXT          Output destination ("-" = stdout).
```

### `prawler comments`

Fetch the comment tree of a submission.

```
Usage: prawler comments [OPTIONS] URL

Arguments:
  URL  Full Reddit submission URL.

Options:
  -d, --depth INTEGER        Maximum comment depth.        [default: 10]
      --min-score INTEGER    Skip comments below this score.
      --include-more         Expand "load more comments" placeholders.
  -f, --filter TEXT          Filter expression. Repeatable.
      --fields TEXT          Comma-separated field projection.
      --format TEXT          Output format.              [default: jsonl]
  -o, --output TEXT          Output destination.
```

### `prawler search`

Full-text search with Reddit's search API.

```
Usage: prawler search [OPTIONS] QUERY

Arguments:
  QUERY  Search query string.

Options:
      --sub TEXT             Subreddit to search (default: all).
  -s, --sort [relevance|hot|top|new|comments]
                                                    [default: relevance]
  -t, --time [hour|day|week|month|year|all]         [default: all]
  -f, --filter TEXT
  -n, --limit INTEGER                               [default: 100]
      --fields TEXT
      --format TEXT                                 [default: jsonl]
  -o, --output TEXT
```

## Filtering

The `--filter` flag accepts expressions of the form `field operator value`. Multiple filters are ANDed together.

| Operator          | Meaning                        | Example                           |
| ----------------- | ------------------------------ | --------------------------------- |
| `=`               | Exact match                    | `flair=Discussion`                |
| `!=`              | Not equal                      | `author!=AutoModerator`           |
| `>=` `<=` `>` `<` | Numeric comparison             | `score>=100`                      |
| `~=`              | Regex match (case-insensitive) | `title~=\[research\]`             |
| `in`              | Value in comma-separated list  | `subreddit in Python,learnpython` |

```bash
# Keep only high-engagement non-stickied posts
prawler posts r/programming \
  --filter "score>=200"          \
  --filter "num_comments>=50"    \
  --filter "stickied=false"      \
  --filter "author!=AutoModerator"
```

Filters are applied lazily in the pipeline — no record is fetched beyond what is needed.

## Output formats

| Format   | Flag                | Best for                                               |
| -------- | ------------------- | ------------------------------------------------------ |
| JSONL    | `--format jsonl`    | Streaming, `pandas.read_json(lines=True)`, large files |
| JSON     | `--format json`     | Small datasets, human inspection                       |
| CSV      | `--format csv`      | R, Excel, any tabular tool                             |
| Table    | `--format table`    | Terminal preview with Rich                             |
| Markdown | `--format markdown` | Reports, GitHub issues                                 |

### Field projection

Use `--fields` to emit only the columns you need, which reduces output size and simplifies downstream processing.

```bash
prawler posts r/MachineLearning --fields id,title,score,url,created_utc,author
```

Available post fields: `id`, `title`, `url`, `permalink`, `score`, `upvote_ratio`, `num_comments`, `created_utc`, `subreddit`, `author`, `selftext`, `is_self`, `flair`, `nsfw`, `spoiler`, `locked`, `stickied`, `domain`, `media_url`.

### Multiple outputs

Write to more than one destination in a single pass — no second crawl required.

```bash
prawler posts r/datasets \
  --format jsonl --output raw/posts.jsonl \
  --format csv   --output summary/posts.csv
```

## Scientific use

Prawler is designed for reproducible data collection. The following features address common requirements in statistical and computational research.

### Crawl manifests

When `reproducibility.write_manifest = true` (the default), every crawl produces a sidecar `.manifest.json` alongside the output file:

```json
{
  "session_id": "a3f1c9b2d047",
  "started_at": "2024-11-12T14:30:00+00:00",
  "finished_at": "2024-11-12T14:37:22+00:00",
  "prawler_version": "0.1.0",
  "praw_version": "7.7.1",
  "config_fingerprint": "3a8f1c9b2d04",
  "command": "posts r/MachineLearning --sort top --time year --limit 500",
  "source": "MachineLearning",
  "filters": ["score>=100"],
  "resolved_seed": 42,
  "records_fetched": 523,
  "records_emitted": 487,
  "records_skipped": 12,
  "records_deduped": 24
}
```

The `config_fingerprint` is a SHA-256 hash of the resolved config (credentials redacted). If any parameter changes between two runs, the fingerprint changes — making configuration drift detectable.

### Reproducible sampling

For large subreddits where a full crawl is impractical, prawler supports three sampling strategies, all controlled by a fixed seed:

```toml
[sampling]
strategy    = "random"   # Bernoulli trial per record
rate        = 0.1        # keep 10%
[reproducibility]
random_seed = 42         # same seed → identical sample
```

```toml
[sampling]
strategy = "systematic"  # keep every Nth record
every_n  = 10            # deterministic, no randomness required
```

### Datetime formats

Configure output datetime precision for your downstream toolchain:

```toml
[temporal]
datetime_format = "unix_ms"   # integer milliseconds — pandas/R friendly
output_timezone = "UTC"       # always UTC internally; converts at output
```

```python
# pandas
df = pd.read_json("posts.jsonl", lines=True)
df["created_utc"] = pd.to_datetime(df["created_utc"], unit="ms", utc=True)

# R
df <- jsonlite::stream_in(file("posts.jsonl"))
df$created_utc <- as.POSIXct(df$created_utc / 1000, origin = "1970-01-01", tz = "UTC")
```

### Completeness guarantees

```toml
[completeness]
require_fields          = ["author", "score", "selftext"]
include_deleted_author  = false   # drop [deleted] posts
include_removed_content = false   # drop [removed] content
min_author_age_days     = 30      # filter throwaway accounts
```

Records that fail completeness checks are counted in the manifest under `records_skipped` — they are never silently dropped.

### Resuming interrupted crawls

```toml
[checkpoint]
enabled          = true
every_n_records  = 1000
```

```bash
# start a long crawl
prawler posts r/science --limit 50000 --format jsonl --output science.jsonl

# if interrupted, resume from the last checkpoint
prawler posts r/science --limit 50000 --format jsonl --output science.jsonl --resume
```

## Configuration

Prawler resolves configuration in layers, from lowest to highest priority:

```
hard-coded defaults → ~/.config/prawler/config.toml → environment variables → CLI flags
```

A fully annotated example config is available at [`config.toml.example`](config.toml.example). The most commonly tuned sections:

```toml
[network]
requests_per_minute = 30    # Reddit OAuth limit is ~60/min; 30 leaves headroom
batch_size          = 100   # items per API request (Reddit hard limit: 100)
max_retries         = 5

[output]
format      = "jsonl"
destination = "-"

[deduplication]
enabled    = true
key_fields = ["id"]         # use ["id", "subreddit"] for multi-subreddit merges
```

All settings are also configurable via environment variables with the `PRAWLER_` prefix and double-underscore nesting, following pydantic-settings conventions:

```bash
PRAWLER_NETWORK__REQUESTS_PER_MINUTE=20
PRAWLER_REPRODUCIBILITY__RANDOM_SEED=99
PRAWLER_TEMPORAL__DATETIME_FORMAT=unix_ms
```

## Development

```bash
# install with dev dependencies
pip install -e ".[dev]"

# run the test suite
pytest

# lint and format
ruff check src/ tests/
ruff format src/ tests/

# type checking
mypy src/
```

### Project structure

```
src/prawler/
├── cli/          # Typer commands and shared option definitions
├── client/       # PRAW wrapper (only module that imports praw)
├── crawler/      # PostCrawler, CommentCrawler — PRAW → domain models
├── pipeline/     # Lazy filter, transform, and enrich stages
├── output/       # Formatter (Strategy) and Sink abstractions
├── model/        # Frozen dataclasses: Post, Comment
└── config.py     # Layered config with pydantic-settings
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for a full design walkthrough including sequence diagrams and architectural decision records.

### Adding a new output format

Implement the `Formatter` protocol and register it in one line:

```python
# src/prawler/output/formatters/ndjson_fmt.py
class NdJsonFormatter:
    def format(self, items):
        for item in items:
            yield json.dumps(item) + "\n"

# src/prawler/output/registry.py
FORMATTERS["ndjson"] = NdJsonFormatter
```

No other changes required.

> **Note on Reddit's Terms of Service** — prawler uses the official Reddit API via PRAW and respects rate limits. Before collecting data at scale, review [Reddit's API Terms of Use](https://redditinc.com/policies/user-agreements) and [Data API Terms](https://www.redditinc.com/policies/data-api-terms). Do not use prawler to scrape personal data or circumvent access controls.
