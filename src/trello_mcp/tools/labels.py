from __future__ import annotations

from fastmcp import FastMCP

from trello_mcp.client import TrelloAPIError

labels_mcp = FastMCP("labels")


@labels_mcp.tool
async def get_labels(board_id: str) -> str:
    """Get all labels defined on a board."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            labels = await client.get_labels(board_id)
        except TrelloAPIError as e:
            return str(e)
    if not labels:
        return "No labels found on this board."
    lines = [f"## Labels ({len(labels)})", ""]
    for lbl in labels:
        lines.append(lbl.to_markdown())
    return "\n".join(lines)


@labels_mcp.tool
async def create_label(board_id: str, name: str, color: str | None = None) -> str:
    """Create a new label on a board."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            label = await client.create_label(board_id, name, color=color)
        except TrelloAPIError as e:
            return str(e)
    return f"Label created.\n\n{label.to_markdown()}"


@labels_mcp.tool
async def delete_label(label_id: str) -> str:
    """Delete a label from a board."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            await client.delete_label(label_id)
        except TrelloAPIError as e:
            return str(e)
    return "Label deleted."


@labels_mcp.tool
async def add_label_to_card(card_id: str, label_id: str) -> str:
    """Add a label to a card."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            await client.add_label_to_card(card_id, label_id)
        except TrelloAPIError as e:
            return str(e)
    return "Label added to card."


@labels_mcp.tool
async def remove_label_from_card(card_id: str, label_id: str) -> str:
    """Remove a label from a card."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            await client.remove_label_from_card(card_id, label_id)
        except TrelloAPIError as e:
            return str(e)
    return "Label removed from card."
