# Scientific Use & Reproducibility

Prawler is designed for reproducible data collection. The following features address common requirements in statistical and computational research.

## Crawl Manifests

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

## Reproducible Sampling

For large subreddits where a full crawl is impractical, prawler supports sampling strategies controlled by a fixed seed:

```toml
[sampling]
strategy    = "random"   # Bernoulli trial per record
rate        = 0.1        # keep 10%
[reproducibility]
random_seed = 42         # same seed → identical sample
```

## Datetime Formats

Configure output datetime precision for your downstream toolchain via `config.toml`:

```toml
[temporal]
datetime_format = "unix_ms"   # integer milliseconds — pandas/R friendly
output_timezone = "UTC"       # always UTC internally; converts at output
```

## Completeness Guarantees

```toml
[completeness]
require_fields          = ["author", "score", "selftext"]
include_deleted_author  = false   # drop [deleted] posts
include_removed_content = false   # drop [removed] content
min_author_age_days     = 30      # filter throwaway accounts
```

Records that fail completeness checks are counted in the manifest under `records_skipped` — they are never silently dropped.

## Resuming Interrupted Crawls

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
