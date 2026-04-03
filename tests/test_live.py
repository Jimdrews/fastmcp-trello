"""Live smoke tests against real Trello API.

Skipped unless TRELLO_API_KEY and TRELLO_TOKEN are set.
"""

import os

import pytest

from trello_mcp.client import TrelloClient

pytestmark = pytest.mark.live

SKIP_REASON = "Set TRELLO_API_KEY and TRELLO_TOKEN to run live tests"


def get_live_client():
    api_key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    if not api_key or not token:
        pytest.skip(SKIP_REASON)
    return TrelloClient(api_key=api_key, token=token)


@pytest.mark.asyncio
async def test_get_boards_live():
    client = get_live_client()
    async with client:
        boards = await client.get_boards()
    assert isinstance(boards, list)
    if boards:
        assert boards[0].name
        assert boards[0].id


@pytest.mark.asyncio
async def test_get_card_live():
    """Requires at least one board with at least one card."""
    client = get_live_client()
    async with client:
        boards = await client.get_boards()
        if not boards:
            pytest.skip("No boards available")

        lists = await client.get_lists(boards[0].id)
        if not lists:
            pytest.skip("No lists available")

        cards = await client.get_cards(lists[0].id)
        if not cards:
            pytest.skip("No cards available")

        card = await client.get_card(cards[0].id)
    assert card.name
    assert card.id
