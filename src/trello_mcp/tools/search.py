from __future__ import annotations

from fastmcp import FastMCP

from trello_mcp.client import TrelloAPIError

search_mcp = FastMCP("search")


@search_mcp.tool
async def add_comment(card_id: str, text: str) -> str:
    """Add a comment to a card."""
    if not text.strip():
        return "Error: Comment text cannot be empty."
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            comment = await client.add_comment(card_id, text)
        except TrelloAPIError as e:
            return str(e)
    return f"Comment added.\n\n{comment.to_markdown()}"


@search_mcp.tool
async def search_cards(query: str, board_id: str | None = None) -> str:
    """Search for cards across boards. Optionally scope to a specific board."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            cards = await client.search_cards(query, board_id=board_id)
        except TrelloAPIError as e:
            return str(e)
    if not cards:
        return "No cards found matching your search."
    lines = [f"## Search Results ({len(cards)})", ""]
    for c in cards:
        parts = [c.to_markdown()]
        if c.board_name:
            parts.append(f"board: {c.board_name}")
        if c.list_name:
            parts.append(f"list: {c.list_name}")
        lines.append(" — ".join(parts))
    return "\n".join(lines)
