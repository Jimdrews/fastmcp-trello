from unittest.mock import patch

import pytest

from trello_mcp.client import TrelloAPIError
from trello_mcp.models import Board, TrelloList
from trello_mcp.tools.boards import (
    close_board,
    create_board,
    get_board,
    get_boards,
    get_lists,
    update_board,
)


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


class TestCreateBoard:
    @pytest.mark.asyncio
    async def test_create(self, mock_client):
        mock_client.create_board.return_value = Board(
            id="board1", name="New Board", url="https://trello.com/b/new"
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_board("New Board")
        assert "Board created" in result
        assert "New Board" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.create_board.side_effect = TrelloAPIError("failed")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_board("New Board")
        assert "failed" in result


class TestUpdateBoard:
    @pytest.mark.asyncio
    async def test_update(self, mock_client):
        mock_client.update_board.return_value = Board(
            id="board1", name="Renamed", url="https://trello.com/b/1"
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_board("board1", name="Renamed")
        assert "Board updated" in result
        assert "Renamed" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.update_board.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_board("board1", name="Renamed")
        assert "Not found" in result


class TestCloseBoard:
    @pytest.mark.asyncio
    async def test_close(self, mock_client):
        mock_client.close_board.return_value = Board(
            id="board1", name="Closed Board", url="https://trello.com/b/1"
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await close_board("board1")
        assert "Board closed" in result
        assert "Closed Board" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.close_board.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await close_board("board1")
        assert "Not found" in result
