from __future__ import annotations

from fastmcp import FastMCP

from trello_mcp.client import TrelloAPIError

boards_mcp = FastMCP("boards")


@boards_mcp.tool
async def get_boards() -> str:
    """List all boards accessible to you."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            boards = await client.get_boards()
        except TrelloAPIError as e:
            return str(e)
    if not boards:
        return "No boards found."
    lines = [f"## Your Boards ({len(boards)})", ""]
    for b in boards:
        lines.append(b.to_compact_markdown())
    return "\n".join(lines)


@boards_mcp.tool
async def get_board(board_id: str) -> str:
    """Get a board's details including its lists."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            board = await client.get_board(board_id)
        except TrelloAPIError as e:
            return str(e)
    return board.to_markdown()


@boards_mcp.tool
async def get_lists(board_id: str) -> str:
    """Get all open lists on a board."""
    from trello_mcp.server import get_client

    async with get_client() as client:
        try:
            lists = await client.get_lists(board_id)
        except TrelloAPIError as e:
            return str(e)
    if not lists:
        return "No lists found on this board."
    lines = [f"## Lists ({len(lists)})", ""]
    for tl in lists:
        lines.append(tl.to_compact_markdown())
    return "\n".join(lines)
