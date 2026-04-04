from unittest.mock import patch

import pytest

from trello_mcp.client import TrelloAPIError
from trello_mcp.models import Label
from trello_mcp.tools.labels import (
    add_label_to_card,
    create_label,
    delete_label,
    get_labels,
    remove_label_from_card,
)


class TestGetLabels:
    @pytest.mark.asyncio
    async def test_returns_labels(self, mock_client, sample_label):
        mock_client.get_labels.return_value = [
            sample_label,
            Label(id="lab2", name="feature", color="green"),
        ]
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_labels("board1")
        assert "bug" in result
        assert "feature" in result
        assert "2" in result

    @pytest.mark.asyncio
    async def test_no_labels(self, mock_client):
        mock_client.get_labels.return_value = []
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_labels("board1")
        assert "No labels found" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.get_labels.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_labels("board1")
        assert "Not found" in result


class TestCreateLabel:
    @pytest.mark.asyncio
    async def test_create(self, mock_client, sample_label):
        mock_client.create_label.return_value = sample_label
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_label("board1", "bug", color="red")
        assert "Label created" in result
        assert "bug" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.create_label.side_effect = TrelloAPIError("failed")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_label("board1", "bug")
        assert "failed" in result


class TestDeleteLabel:
    @pytest.mark.asyncio
    async def test_delete(self, mock_client):
        mock_client.delete_label.return_value = None
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await delete_label("lab1")
        assert "Label deleted" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.delete_label.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await delete_label("lab1")
        assert "Not found" in result


class TestAddLabelToCard:
    @pytest.mark.asyncio
    async def test_add(self, mock_client):
        mock_client.add_label_to_card.return_value = None
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_label_to_card("card1", "lab1")
        assert "Label added" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.add_label_to_card.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_label_to_card("card1", "lab1")
        assert "Not found" in result


class TestRemoveLabelFromCard:
    @pytest.mark.asyncio
    async def test_remove(self, mock_client):
        mock_client.remove_label_from_card.return_value = None
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await remove_label_from_card("card1", "lab1")
        assert "Label removed" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.remove_label_from_card.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await remove_label_from_card("card1", "lab1")
        assert "Not found" in result
