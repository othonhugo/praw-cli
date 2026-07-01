# Data Processing (Pipelines)

Prawler features a **Pipeline** engine that allows you to filter and project data _before_ sending it to the output. This avoids unnecessary API traffic and guarantees sanitized datasets out of the box.

## Filtering (`--filter` / `-F`)

You can use multiple `--filter` flags to apply conditions in sequence. Filters support the following operations:

- `=` / `!=`: Exact equality and inequality.
- `>`, `<`, `>=`, `<=`: Numerical and date comparisons.
- `~=`: Regular Expression (case-insensitive).
- `in`: Checks if the exact string is in a comma-separated list.
- `has`: Checks if **any** of the comma-separated keywords are contained in the text.
- `has_all`: Checks if **all** of the comma-separated keywords are contained in the text.
- `starts_with` / `ends_with`: Checks for textual prefix or suffix.
- `len>=`, `len<=`, `len>`, `len<`, `len=`: Checks string character length (great for NLP preprocessing).

> [!TIP]
> **Data Science Tip:** Numerical operators (`>=`, `<=`, etc.) also automatically compare dates (ISO-8601 strings). Therefore, you can natively filter by date using `created_utc >= 2024-01-01`.

### Filter Usage Examples

```bash
# 1. Equality and Inequality (ignore bot accounts)
prawler posts python --filter "author!=AutoModerator"

# 2. Numerical and Date Comparisons
prawler posts python --filter "score>100" --filter "created_utc>=2024-01-01"

# 3. Regular Expression (titles containing the word "bot")
prawler posts python --filter "title~=\bbot\b"

# 4. Exact List Matching
prawler comments xyz123 --filter "author in spez,AutoModerator,reddit"

# 5. Contains Any Keyword (OR logic)
prawler posts programming --filter "title has python,golang,rust"

# 6. Contains All Keywords (AND logic)
prawler posts programming --filter "title has_all tutorial,beginner"

# 7. Starts/Ends with (direct links to JPG images)
prawler posts pics --filter "url ends_with .jpg"

# 8. Character Length (NLP / Text Mining)
prawler posts datascience --filter "selftext len>= 500"
```

## Field Projection (`--fields`)

Reduce output size by extracting only the desired fields from the schema.

- **Example:**
  ```bash
  prawler posts programming --fields id,title,score,url,author
  ```

Available fields vary depending on the target entity (Post vs Comment), but common fields include:

- `id`
- `author`
- `score`
- `created_utc`
- `selftext` (for Posts) or `body` (for Comments)
