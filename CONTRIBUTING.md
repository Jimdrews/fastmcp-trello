# Contributing

Thanks for your interest in contributing to fastmcp-trello!

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Jimdrews/fastmcp-trello.git
   cd fastmcp-trello
   ```
2. Install dependencies:
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

1. Fork the repository and clone your fork
2. Create a branch for your change (`git checkout -b my-change`)
3. Make your changes and add tests where appropriate
4. Ensure all checks pass: `uv run pytest && uv run ruff check && uv run ruff format --check`
5. Push your branch and open a pull request against `main`

Note: Direct pushes to `main` are restricted to maintainers. All external contributions must go through a pull request.