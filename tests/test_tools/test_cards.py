import pytest
from unittest.mock import patch

from trello_mcp.client import TrelloAPIError
from trello_mcp.models import Card
from trello_mcp.tools.cards import (
    get_cards,
    get_card,
    create_card,
    update_card,
    archive_card,
)


class TestGetCards:
    @pytest.mark.asyncio
    async def test_returns_cards(self, mock_client):
        mock_client.get_cards.return_value = [
            Card(id="card1", name="Fix bug", closed=False),
            Card(id="card2", name="Add feature", closed=False),
        ]
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_cards("list1")
        assert "Fix bug" in result
        assert "Add feature" in result
        assert "2" in result

    @pytest.mark.asyncio
    async def test_empty_list(self, mock_client):
        mock_client.get_cards.return_value = []
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_cards("list1")
        assert "No cards" in result


class TestGetCard:
    @pytest.mark.asyncio
    async def test_returns_full_card(self, mock_client, sample_card):
        mock_client.get_card.return_value = sample_card
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_card("card1")
        assert "Fix login timeout" in result
        assert "Doing" in result
        assert "Sprint 42" in result
        assert "bug" in result
        assert "Reproduced on staging" in result

    @pytest.mark.asyncio
    async def test_invalid_card(self, mock_client):
        mock_client.get_card.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_card("nonexistent")
        assert "Not found" in result


class TestCreateCard:
    @pytest.mark.asyncio
    async def test_create_minimal(self, mock_client):
        mock_client.create_card.return_value = Card(
            id="new1", name="New task", closed=False
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_card(list_id="list1", name="New task")
        assert "Card created" in result
        assert "New task" in result

    @pytest.mark.asyncio
    async def test_create_with_options(self, mock_client):
        mock_client.create_card.return_value = Card(
            id="new2",
            name="Detailed task",
            desc="Some details",
            due="2026-05-01T00:00:00.000Z",
            closed=False,
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_card(
                list_id="list1",
                name="Detailed task",
                description="Some details",
                due="2026-05-01",
            )
        assert "Card created" in result
        assert "Detailed task" in result

    @pytest.mark.asyncio
    async def test_create_invalid_list(self, mock_client):
        mock_client.create_card.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_card(list_id="bad", name="Task")
        assert "Not found" in result


class TestUpdateCard:
    @pytest.mark.asyncio
    async def test_update_name(self, mock_client):
        mock_client.update_card.return_value = Card(
            id="card1", name="Updated name", closed=False
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_card(card_id="card1", name="Updated name")
        assert "Card updated" in result
        assert "Updated name" in result

    @pytest.mark.asyncio
    async def test_move_card(self, mock_client):
        mock_client.update_card.return_value = Card(
            id="card1", name="Task", closed=False
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_card(card_id="card1", list_id="list2")
        assert "Card updated" in result
        mock_client.update_card.assert_called_once_with(
            "card1", name=None, desc=None, due=None, list_id="list2"
        )

    @pytest.mark.asyncio
    async def test_update_multiple_fields(self, mock_client):
        mock_client.update_card.return_value = Card(
            id="card1", name="New name", desc="New desc", closed=False
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_card(
                card_id="card1", name="New name", description="New desc"
            )
        assert "Card updated" in result

    @pytest.mark.asyncio
    async def test_update_invalid_card(self, mock_client):
        mock_client.update_card.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_card(card_id="bad", name="X")
        assert "Not found" in result


class TestArchiveCard:
    @pytest.mark.asyncio
    async def test_archive(self, mock_client):
        mock_client.archive_card.return_value = Card(
            id="card1", name="Archived task", closed=True
        )
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await archive_card("card1")
        assert "Card archived" in result
        assert "Archived task" in result

    @pytest.mark.asyncio
    async def test_archive_invalid(self, mock_client):
        mock_client.archive_card.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await archive_card("bad")
        assert "Not found" in result
