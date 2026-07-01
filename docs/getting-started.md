# Getting Started

Welcome to Prawler! This guide will help you install the tool, set up your Reddit API credentials, and run your first extraction.

## Installation

Prawler uses `uv` for dependency management and virtual environments. To install and configure the tool, follow the steps below:

```bash
# 1. Enter the project directory
cd prawler

# 2. Install dependencies and the current package into the virtual environment
uv sync

# 3. Activate the newly created virtual environment
source .venv/bin/activate

# 4. The `prawler` command is now available in your terminal!
prawler --help
```

## Authentication (Environment Variables)

To use Prawler, you must authenticate with the Reddit API. We use environment variables to ensure your credentials are never saved in your terminal history or accidentally committed to source control.

The following variables are supported:

| Variable                | Description                                     | Required                    |
| ----------------------- | ----------------------------------------------- | --------------------------- |
| `PRAWLER_CLIENT_ID`     | Your Reddit application Client ID.              | **Yes**                     |
| `PRAWLER_CLIENT_SECRET` | Your Reddit application Client Secret.          | **Yes**                     |
| `PRAWLER_USER_AGENT`    | A descriptive name for your bot.                | No (Default: `prawler/0.2`) |
| `PRAWLER_USERNAME`      | Your Reddit username (for user-scoped actions). | No                          |
| `PRAWLER_PASSWORD`      | Your Reddit password (for user-scoped actions). | No                          |

**Quick usage example:**

```bash
export PRAWLER_CLIENT_ID="your_client_id_here"
export PRAWLER_CLIENT_SECRET="your_client_secret_here"

# Test your authentication by fetching posts:
prawler posts python
```

You can also add these variables to a local `.env` file if your environment loads variables automatically, or pass them inline:

```bash
PRAWLER_CLIENT_ID="id" PRAWLER_CLIENT_SECRET="secret" prawler search "API"
```

## Next Steps

Now that you have Prawler installed and authenticated, check out the core CLI commands:

- [CLI Commands Guide](usage/commands.md)
- [Pipelines & Filtering](usage/pipelines-filters.md)
