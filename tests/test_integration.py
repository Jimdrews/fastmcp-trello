"""Integration tests calling all 10 tools through FastMCP in-memory client."""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client

from trello_mcp.client import TrelloClient
from trello_mcp.models import Board, Card, Comment, Label, Member, TrelloList
from trello_mcp.server import mcp


@pytest.fixture
def mock_client():
    client = AsyncMock(spec=TrelloClient)
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)

    # Boards
    client.get_boards.return_value = [
        Board(id="board1", name="Sprint 42", url="https://trello.com/b/1"),
    ]
    client.get_board.return_value = Board(
        id="board1",
        name="Sprint 42",
        url="https://trello.com/b/1",
        lists=[TrelloList(id="list1", name="To Do", card_count=3)],
    )
    client.get_lists.return_value = [
        TrelloList(id="list1", name="To Do"),
        TrelloList(id="list2", name="Doing"),
    ]

    # Cards
    card = Card(
        id="card1",
        name="Fix bug",
        desc="A bug",
        closed=False,
        list_name="Doing",
        board_name="Sprint 42",
        labels=[Label(id="lab1", name="bug", color="red")],
        members=[Member(id="mem1", username="james", full_name="James")],
        comments=[
            Comment(
                id="com1",
                text="Found it",
                date="2026-03-28T10:00:00.000Z",
                member_creator=Member(id="mem2", username="sarah", full_name="Sarah"),
            )
        ],
    )
    client.get_cards.return_value = [card]
    client.get_card.return_value = card
    client.create_card.return_value = Card(id="new1", name="New", closed=False)
    client.update_card.return_value = Card(id="card1", name="Updated", closed=False)
    client.archive_card.return_value = Card(id="card1", name="Archived", closed=True)

    # Comments & Search
    client.add_comment.return_value = Comment(
        id="com2",
        text="Nice!",
        date="2026-04-01T12:00:00.000Z",
        member_creator=Member(id="mem1", username="james", full_name="James"),
    )
    client.search_cards.return_value = [card]

    return client


@pytest.mark.asyncio
async def test_all_tools_through_mcp(mock_client):
    """Verify all 10 tools are callable through the MCP protocol."""
    with patch("trello_mcp.server.get_client", return_value=mock_client):
        async with Client(transport=mcp) as c:
            tools = await c.list_tools()
            tool_names = {t.name for t in tools}
            assert tool_names == {
                "get_boards",
                "get_board",
                "get_lists",
                "get_cards",
                "get_card",
                "create_card",
                "update_card",
                "archive_card",
                "add_comment",
                "search_cards",
            }

            # Call each tool and verify it returns text
            result = await c.call_tool("get_boards", {})
            assert "Sprint 42" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool("get_board", {"board_id": "board1"})
            assert "Sprint 42" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool("get_lists", {"board_id": "board1"})
            assert "To Do" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool("get_cards", {"list_id": "list1"})
            assert "Fix bug" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool("get_card", {"card_id": "card1"})
            assert "Fix bug" in result.content[0].text  # pyrefly: ignore [missing-attribute]
            assert "Doing" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool(
                "create_card", {"list_id": "list1", "name": "New"}
            )
            assert "Card created" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool(
                "update_card", {"card_id": "card1", "name": "Updated"}
            )
            assert "Card updated" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool("archive_card", {"card_id": "card1"})
            assert "Card archived" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool(
                "add_comment", {"card_id": "card1", "text": "Nice!"}
            )
            assert "Comment added" in result.content[0].text  # pyrefly: ignore [missing-attribute]

            result = await c.call_tool("search_cards", {"query": "bug"})
            assert "Fix bug" in result.content[0].text  # pyrefly: ignore [missing-attribute]
