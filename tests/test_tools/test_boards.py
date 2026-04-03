from unittest.mock import patch

import pytest

from trello_mcp.client import TrelloAPIError
from trello_mcp.models import Board, TrelloList
from trello_mcp.tools.boards import get_board, get_boards, get_lists


class TestGetBoards:
    @pytest.mark.asyncio
    async def test_returns_boards(self, mock_client, sample_board):
        mock_client.get_boards.return_value = [
            sample_board,
            Board(id="board2", name="Backlog", url="https://trello.com/b/2"),
        ]
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_boards()
        assert "Sprint 42" in result
        assert "Backlog" in result
        assert "2" in result  # count

    @pytest.mark.asyncio
    async def test_no_boards(self, mock_client):
        mock_client.get_boards.return_value = []
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_boards()
        assert "No boards found" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.get_boards.side_effect = TrelloAPIError("Authentication failed")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_boards()
        assert "Authentication failed" in result


class TestGetBoard:
    @pytest.mark.asyncio
    async def test_returns_board_with_lists(self, mock_client, sample_board):
        mock_client.get_board.return_value = sample_board
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_board("board1")
        assert "Sprint 42" in result
        assert "To Do" in result
        assert "Doing" in result

    @pytest.mark.asyncio
    async def test_invalid_board(self, mock_client):
        mock_client.get_board.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_board("nonexistent")
        assert "Not found" in result


class TestGetLists:
    @pytest.mark.asyncio
    async def test_returns_lists(self, mock_client):
        mock_client.get_lists.return_value = [
            TrelloList(id="list1", name="To Do"),
            TrelloList(id="list2", name="Doing"),
        ]
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_lists("board1")
        assert "To Do" in result
        assert "Doing" in result

    @pytest.mark.asyncio
    async def test_empty_board(self, mock_client):
        mock_client.get_lists.return_value = []
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_lists("board1")
        assert "No lists found" in result
