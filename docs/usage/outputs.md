# Formatters and Export (Outputs)

You can direct the output of your collections to the console or to local files in multiple formats.

## Supported Formats (`--format` / `-f`)

- `jsonl` (Default) - One JSON object per line. Ideal for large pipelines, streaming data, and easy ingestion into Pandas (`pandas.read_json(lines=True)`).
- `json` - Indented, pretty-printed JSON file. Best for human inspection of small datasets.
- `csv` - Standard tabular CSV format.
- `table` - Stylized terminal table (requires the `rich` package). Great for previews.
- `markdown` - Markdown-formatted table. Best for GitHub issues and reports.

## Output Destination (`--output` / `-o`)

By default, output is printed to `stdout` (`-`). If a file path is provided, it saves the data directly to that file.

- **Combined Examples:**

  ```bash
  # Save search results to a clean CSV file
  prawler search "API" --format csv --output results.csv

  # Print top posts to the terminal in a rich table containing only 3 columns
  prawler posts python --sort top --limit 10 --fields title,score,author --format table
  ```

## Multiple outputs

Write to more than one destination in a single pass — no second crawl required.
(Currently supported natively via configuration or code level).
