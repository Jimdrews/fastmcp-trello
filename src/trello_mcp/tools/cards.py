from __future__ import annotations

from fastmcp import FastMCP

from trello_mcp.client import TrelloAPIError

cards_mcp = FastMCP("cards")


@cards_mcp.tool
async def get_cards(list_id: str) -> str:
    """Get all cards in a list."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            cards = await client.get_cards(list_id)
        except TrelloAPIError as e:
            return str(e)
    if not cards:
        return "No cards in this list."
    lines = [f"## Cards ({len(cards)})", ""]
    for c in cards:
        lines.append(c.to_markdown())
    return "\n".join(lines)


@cards_mcp.tool
async def get_card(card_id: str) -> str:
    """Get full details for a card including comments."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            card = await client.get_card(card_id)
        except TrelloAPIError as e:
            return str(e)
    return card.to_markdown()


@cards_mcp.tool
async def create_card(
    list_id: str,
    name: str,
    description: str | None = None,
    due: str | None = None,
) -> str:
    """Create a new card on a list."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            card = await client.create_card(
                list_id=list_id, name=name, desc=description, due=due
            )
        except TrelloAPIError as e:
            return str(e)
    return f"Card created.\n\n{card.to_markdown()}"


@cards_mcp.tool
async def update_card(
    card_id: str,
    name: str | None = None,
    description: str | None = None,
    due: str | None = None,
    list_id: str | None = None,
) -> str:
    """Update a card's fields. Set list_id to move the card to a different list."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            card = await client.update_card(
                card_id, name=name, desc=description, due=due, list_id=list_id
            )
        except TrelloAPIError as e:
            return str(e)
    return f"Card updated.\n\n{card.to_markdown()}"


@cards_mcp.tool
async def archive_card(card_id: str) -> str:
    """Archive (close) a card."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            card = await client.archive_card(card_id)
        except TrelloAPIError as e:
            return str(e)
    return f"Card archived: **{card.name}**"
