from __future__ import annotations

from fastmcp import FastMCP

from trello_mcp.client import TrelloAPIError

attachments_mcp = FastMCP("attachments")


@attachments_mcp.tool
async def get_attachments(card_id: str) -> str:
    """Get all attachments on a card."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            attachments = await client.get_attachments(card_id)
        except TrelloAPIError as e:
            return str(e)
    if not attachments:
        return "No attachments on this card."
    lines = [f"## Attachments ({len(attachments)})", ""]
    for att in attachments:
        lines.append(att.to_markdown())
    return "\n".join(lines)


@attachments_mcp.tool
async def add_attachment(card_id: str, url: str, name: str | None = None) -> str:
    """Add a URL attachment to a card. Only URLs are supported (no file uploads)."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            att = await client.add_attachment(card_id, url, name=name)
        except TrelloAPIError as e:
            return str(e)
    return f"Attachment added.\n\n{att.to_markdown()}"


@attachments_mcp.tool
async def delete_attachment(card_id: str, attachment_id: str) -> str:
    """Delete an attachment from a card."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            await client.delete_attachment(card_id, attachment_id)
        except TrelloAPIError as e:
            return str(e)
    return "Attachment deleted."
