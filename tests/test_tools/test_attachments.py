from unittest.mock import patch

import pytest

from trello_mcp.client import TrelloAPIError
from trello_mcp.tools.attachments import (
    add_attachment,
    delete_attachment,
    get_attachments,
)


class TestGetAttachments:
    @pytest.mark.asyncio
    async def test_returns_attachments(self, mock_client, sample_attachment):
        mock_client.get_attachments.return_value = [sample_attachment]
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_attachments("card1")
        assert "screenshot.png" in result
        assert "1" in result

    @pytest.mark.asyncio
    async def test_no_attachments(self, mock_client):
        mock_client.get_attachments.return_value = []
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_attachments("card1")
        assert "No attachments" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.get_attachments.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await get_attachments("card1")
        assert "Not found" in result


class TestAddAttachment:
    @pytest.mark.asyncio
    async def test_add(self, mock_client, sample_attachment):
        mock_client.add_attachment.return_value = sample_attachment
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_attachment("card1", "https://example.com/screenshot.png")
        assert "Attachment added" in result
        assert "screenshot.png" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.add_attachment.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await add_attachment("card1", "https://example.com")
        assert "Not found" in result


class TestDeleteAttachment:
    @pytest.mark.asyncio
    async def test_delete(self, mock_client):
        mock_client.delete_attachment.return_value = None
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await delete_attachment("card1", "att1")
        assert "Attachment deleted" in result

    @pytest.mark.asyncio
    async def test_api_error(self, mock_client):
        mock_client.delete_attachment.side_effect = TrelloAPIError("Not found")
        with patch("trello_mcp.server.get_client", return_value=mock_client):
            result = await delete_attachment("card1", "att1")
        assert "Not found" in result
