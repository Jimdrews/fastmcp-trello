from __future__ import annotations

from fastmcp import FastMCP

from trello_mcp.client import TrelloAPIError

lists_mcp = FastMCP("lists")


@lists_mcp.tool
async def create_list(board_id: str, name: str, position: str | None = None) -> str:
    """Create a new list on a board. Position can be 'top', 'bottom', or a number."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            tl = await client.create_list(board_id, name, position=position)
        except TrelloAPIError as e:
            return str(e)
    return f"List created.\n\n{tl.to_markdown()}"


@lists_mcp.tool
async def update_list(list_id: str, name: str) -> str:
    """Rename a list."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            tl = await client.update_list(list_id, name)
        except TrelloAPIError as e:
            return str(e)
    return f"List renamed.\n\n{tl.to_markdown()}"


@lists_mcp.tool
async def archive_list(list_id: str) -> str:
    """Archive (close) a list."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            tl = await client.archive_list(list_id)
        except TrelloAPIError as e:
            return str(e)
    return f"List archived: **{tl.name}**"


@lists_mcp.tool
async def move_list(list_id: str, position: str) -> str:
    """Move a list to a new position. Use 'top', 'bottom', or a number."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            tl = await client.move_list(list_id, position)
        except TrelloAPIError as e:
            return str(e)
    return f"List moved: **{tl.name}**"
