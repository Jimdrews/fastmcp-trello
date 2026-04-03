# Contributing

Thanks for your interest in contributing to fastmcp-trello!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/fastmcp-trello.git
   cd fastmcp-trello
   ```
3. Install dependencies:
   ```bash
   uv sync --group dev
   ```

## Development

Run the test suite:

```bash
uv run pytest
```

Run linting and formatting checks:

```bash
uv run ruff check
uv run ruff format --check
```

## Submitting Changes

1. Create a branch for your change
2. Make your changes and add tests where appropriate
3. Ensure all checks pass: `uv run pytest && uv run ruff check && uv run ruff format --check`
4. Open a pull request
