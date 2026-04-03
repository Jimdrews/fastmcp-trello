import pytest
from unittest.mock import patch

from trello_mcp.client import TrelloAPIError
from trello_mcp.models import Card
from trello_mcp.tools.search import add_comment, search_cards


class TestAddComment:
    @pytest.mark.asyncio
    async def test_add_comment(self, mock_client, sample_comment):
        mock_client.add_comment.return_value = sample_comment
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_comment("card1", "Great progress!")
        assert "Comment added" in result
        assert "Great progress!" in result

    @pytest.mark.asyncio
    async def test_invalid_card(self, mock_client):
        mock_client.add_comment.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_comment("bad", "Hello")
        assert "Not found" in result

    @pytest.mark.asyncio
    async def test_empty_text(self, mock_client):
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_comment("card1", "")
        assert "cannot be empty" in result
        mock_client.add_comment.assert_not_called()

    @pytest.mark.asyncio
    async def test_whitespace_only_text(self, mock_client):
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_comment("card1", "   ")
        assert "cannot be empty" in result


class TestSearchCards:
    @pytest.mark.asyncio
    async def test_search_with_results(self, mock_client):
        mock_client.search_cards.return_value = [
            Card(
                id="card1",
                name="Fix login",
                closed=False,
                board_name="Sprint 42",
                list_name="Doing",
            ),
        ]
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await search_cards("login")
        assert "Fix login" in result
        assert "Sprint 42" in result
        assert "Doing" in result

    @pytest.mark.asyncio
    async def test_search_scoped_to_board(self, mock_client):
        mock_client.search_cards.return_value = []
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await search_cards("login", board_id="board1")
        mock_client.search_cards.assert_called_once_with("login", board_id="board1")

    @pytest.mark.asyncio
    async def test_no_results(self, mock_client):
        mock_client.search_cards.return_value = []
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await search_cards("nonexistent")
        assert "No cards found" in result
