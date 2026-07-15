# CLI Commands

The CLI is divided into the following commands.

## Collect Posts (`posts`)

Extracts posts (submissions) from a specific subreddit.

- **Basic syntax:**

  ```bash
  praw-cli posts <subreddit_name>
  ```

  _(Optional: you can omit the `r/` prefix)_

- **Examples:**

  ```bash
  # Collect the top 100 "hot" posts (default) from r/python
  praw-cli posts python

  # Collect the top 500 most upvoted posts of all time from r/programming
  praw-cli posts programming --sort top --time all --limit 500
  ```

## Collect Comments (`comments`)

Extracts comments based on a post URL, post ID, or username.

- **Basic syntax:**

  ```bash
  praw-cli comments <URL | ID | u/username>
  ```

- **Examples:**

  ```bash
  # Collect comments using the post URL
  praw-cli comments https://reddit.com/r/python/comments/xyz123/example/

  # Collect comments by post ID
  praw-cli comments xyz123

  # Collect recent comments from a specific user
  praw-cli comments u/AutoModerator
  ```

## Search Posts (`search`)

Performs searches using Reddit's native search engine.

- **Basic syntax:**

  ```bash
  praw-cli search "your query"
  ```

- **Examples:**

  ```bash
  # Search for "machine learning" across all of Reddit
  praw-cli search "machine learning"

  # Search only within the r/dataengineering subreddit
  praw-cli search "pipeline" --sub dataengineering

  # Sort search results by number of comments
  praw-cli search "python" --sort comments
  ```

## User Data (`user`)

Focuses on extracting data related to a user profile (Redditor).

- **Basic syntax:**

  ```bash
  praw-cli user <username> --mode <posts | comments | profile>
  ```

- **Examples:**

  ```bash
  # Return user profile metadata
  praw-cli user spez --mode profile

  # Return recent posts made by the user
  praw-cli user spez --mode posts

  # Return recent comments made by the user
  praw-cli user spez --mode comments
  ```

## Offline Processing (`input`)

Re-process a previously saved file through the full filter/output pipeline — without making any API requests. Credentials are not needed.

This is useful for:

- **Re-filtering** archived datasets with new criteria.
- **Format conversion** (e.g., `.jsonl` → `.csv` or Markdown).
- **Testing pipelines** locally before running a live crawl.
- **Reproducible analysis** of a snapshot collected at a fixed point in time.

All `--filter`, `--fields`, `--limit`, `--format`, and `--output` flags work exactly the same as in the other commands.

- **Basic syntax:**

  ```bash
  praw-cli input <file>
  ```

  Use `-` as `<file>` to read from **stdin**.

- **Supported input formats (`--input-format`):**

  | Format  | Extension(s)        | Notes                              |
  | ------- | ------------------- | ---------------------------------- |
  | `jsonl` | `.jsonl`, `.ndjson` | Default. One JSON object per line. |
  | `json`  | `.json`             | A JSON array `[{...}, {...}]`.     |
  | `csv`   | `.csv`              | All values are read as strings.    |

  The format is **auto-detected from the file extension** when `--input-format` is omitted. For stdin or extension-less files, pass `--input-format` explicitly.

> [!WARNING]
> **CSV and numeric filters**: `csv.DictReader` reads all column values as plain strings. Filters like `score>=100` will use lexicographic string comparison (`"42" >= "100"` is `True`). For reliable numeric filtering on CSV inputs, convert the file to JSONL first using a previous `praw-cli` run, or use `json` format which preserves native types.

- **Examples:**

  ```bash
  # Re-filter a saved dataset and convert to CSV
  praw-cli input posts.jsonl --filter "score>=500" --format csv --output filtered.csv

  # Project only 3 fields and preview as a terminal table
  praw-cli input posts.jsonl --fields title,score,author --format table

  # Convert a JSON array dump to JSONL
  praw-cli input dump.json --input-format json --format jsonl --output dump.jsonl

  # Pipe from stdin (format must be explicit)
  cat posts.jsonl | praw-cli input - --input-format jsonl --format markdown

  # Limit to first 50 records
  praw-cli input large_dataset.jsonl --limit 50 --format csv --output sample.csv
  ```
