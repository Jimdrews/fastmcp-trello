from unittest.mock import patch

import pytest

from trello_mcp.client import TrelloAPIError
from trello_mcp.models import TrelloList
from trello_mcp.tools.lists import archive_list, create_list, move_list, update_list


class TestCreateList:
    @pytest.mark.asyncio
    async def test_create(self, mock_client):
        mock_client.create_list.return_value = TrelloList(id="list1", name="Backlog")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_list("board1", "Backlog")
        assert "List created" in result
        assert "Backlog" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.create_list.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await create_list("board1", "Backlog")
        assert "Not found" in result


class TestUpdateList:
    @pytest.mark.asyncio
    async def test_rename(self, mock_client):
        mock_client.update_list.return_value = TrelloList(id="list1", name="Renamed")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_list("list1", "Renamed")
        assert "List renamed" in result
        assert "Renamed" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.update_list.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await update_list("list1", "Renamed")
        assert "Not found" in result


class TestArchiveList:
    @pytest.mark.asyncio
    async def test_archive(self, mock_client):
        mock_client.archive_list.return_value = TrelloList(id="list1", name="Old List")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await archive_list("list1")
        assert "List archived" in result
        assert "Old List" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.archive_list.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await archive_list("list1")
        assert "Not found" in result


class TestMoveList:
    @pytest.mark.asyncio
    async def test_move(self, mock_client):
        mock_client.move_list.return_value = TrelloList(id="list1", name="Moved")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await move_list("list1", "top")
        assert "List moved" in result
        assert "Moved" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.move_list.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await move_list("list1", "top")
        assert "Not found" in result
