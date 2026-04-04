<p align="center">
  <img src="banner.svg" alt="fastmcp-trello" width="100%">
</p>

[![PyPI](https://badge.fury.io/py/fastmcp-trello.svg)](https://pypi.org/project/fastmcp-trello/)
[![Python](https://img.shields.io/pypi/pyversions/fastmcp-trello?style=flat)](https://pypi.org/project/fastmcp-trello/)
[![CI](https://github.com/Jimdrews/fastmcp-trello/actions/workflows/ci.yml/badge.svg)](https://github.com/Jimdrews/fastmcp-trello/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Trello MCP server — manage boards, cards, and lists from any AI assistant that supports the [Model Context Protocol](https://modelcontextprotocol.io). MCP is an open standard that lets AI assistants like Claude, Cursor, and Copilot interact with external tools and services.

## Trello MCP Tools

| Tool | Description |
|---|---|
| `get_boards` | List all boards accessible to you |
| `get_board` | Get a board's details including its lists |
| `get_lists` | Get all open lists on a board |
| `get_cards` | Get all cards in a list |
| `get_card` | Get full details for a card including comments |
| `create_card` | Create a new card on a list |
| `update_card` | Update a card's fields or move it to a different list |
| `archive_card` | Archive (close) a card |
| `add_comment` | Add a comment to a card |
| `search_cards` | Search for cards across boards, optionally scoped to a specific board |

## Prerequisites

You need a Trello API key and token:

1. Go to the [Trello Power-Ups admin page](https://trello.com/power-ups/admin)
2. Create a new Power-Up (any name/workspace will do)
3. Generate a new API key
4. From the API key page, click the **Token** link to generate a token

## Installation

### Claude Desktop

Add to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "trello": {
      "command": "uvx",
      "args": ["fastmcp-trello"],
      "env": {
        "TRELLO_API_KEY": "your-api-key",
        "TRELLO_TOKEN": "your-token"
      }
    }
  }
}
```

### VS Code

Add to your VS Code MCP settings (`.vscode/mcp.json`):

```json
{
  "servers": {
    "trello": {
      "command": "uvx",
      "args": ["fastmcp-trello"],
      "env": {
        "TRELLO_API_KEY": "your-api-key",
        "TRELLO_TOKEN": "your-token"
      }
    }
  }
}
```

### Cursor

Add to your Cursor MCP settings (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "trello": {
      "command": "uvx",
      "args": ["fastmcp-trello"],
      "env": {
        "TRELLO_API_KEY": "your-api-key",
        "TRELLO_TOKEN": "your-token"
      }
    }
  }
}
```

### Standalone

```bash
# Run directly (no install needed)
uvx fastmcp-trello

# Or install globally
pip install fastmcp-trello
fastmcp-trello

# Use HTTP transport instead of stdio
fastmcp-trello --transport http
```

## Usage

Once installed in your MCP client, you can ask your AI assistant things like:

> "Show me all my Trello boards"

> "Create a card called 'Fix login bug' in the To Do list on my Project board"

## Configuration

| Variable | Required | Description |
|---|---|---|
| `TRELLO_API_KEY` | Yes | Your Trello API key |
| `TRELLO_TOKEN` | Yes | Your Trello authentication token |

## Development

```bash
git clone https://github.com/Jimdrews/fastmcp-trello.git
cd fastmcp-trello
uv sync --group dev
uv run pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

[MIT](LICENSE)

<!-- mcp-name: io.github.jimdrews/fastmcp-trello -->
