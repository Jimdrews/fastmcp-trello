from __future__ import annotations

import os

from fastmcp import FastMCP

from trello_mcp.client import TrelloClient
from trello_mcp.tools.attachments import attachments_mcp
from trello_mcp.tools.boards import boards_mcp
from trello_mcp.tools.cards import cards_mcp
from trello_mcp.tools.labels import labels_mcp
from trello_mcp.tools.lists import lists_mcp
from trello_mcp.tools.search import search_mcp

mcp = FastMCP("trello")

mcp.mount(attachments_mcp)
mcp.mount(boards_mcp)
mcp.mount(cards_mcp)
mcp.mount(labels_mcp)
mcp.mount(lists_mcp)
mcp.mount(search_mcp)


def get_client() -> TrelloClient:
    api_key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    if not api_key:
        raise ValueError("TRELLO_API_KEY environment variable is required")
    if not token:
        raise ValueError("TRELLO_TOKEN environment variable is required")
    return TrelloClient(api_key=api_key, token=token)


if __name__ == "__main__":
    mcp.run()
