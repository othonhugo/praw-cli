# CLI Commands

The CLI is divided into four main commands, targeting different Reddit entities.

## Collect Posts (`posts`)

Extracts posts (submissions) from a specific subreddit.

- **Basic syntax:**

  ```bash
  prawler posts <subreddit_name>
  ```

  _(Optional: you can omit the `r/` prefix)_

- **Examples:**

  ```bash
  # Collect the top 100 "hot" posts (default) from r/python
  prawler posts python

  # Collect the top 500 most upvoted posts of all time from r/programming
  prawler posts programming --sort top --time all --limit 500
  ```

## Collect Comments (`comments`)

Extracts comments based on a post URL, post ID, or username.

- **Basic syntax:**

  ```bash
  prawler comments <URL | ID | u/username>
  ```

- **Examples:**

  ```bash
  # Collect comments using the post URL
  prawler comments https://reddit.com/r/python/comments/xyz123/example/

  # Collect comments by post ID
  prawler comments xyz123

  # Collect recent comments from a specific user
  prawler comments u/AutoModerator
  ```

## Search Posts (`search`)

Performs searches using Reddit's native search engine.

- **Basic syntax:**

  ```bash
  prawler search "your query"
  ```

- **Examples:**

  ```bash
  # Search for "machine learning" across all of Reddit
  prawler search "machine learning"

  # Search only within the r/dataengineering subreddit
  prawler search "pipeline" --sub dataengineering

  # Sort search results by number of comments
  prawler search "python" --sort comments
  ```

## User Data (`user`)

Focuses on extracting data related to a user profile (Redditor).

- **Basic syntax:**

  ```bash
  prawler user <username> --mode <posts | comments | profile>
  ```

- **Examples:**

  ```bash
  # Return user profile metadata
  prawler user spez --mode profile

  # Return recent posts made by the user
  prawler user spez --mode posts

  # Return recent comments made by the user
  prawler user spez --mode comments
  ```
