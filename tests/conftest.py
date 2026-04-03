import pytest
from unittest.mock import AsyncMock

from trello_mcp.client import TrelloClient
from trello_mcp.models import Board, Card, Comment, Label, Member, TrelloList


@pytest.fixture
def mock_client():
    """Create a mock TrelloClient with all methods as AsyncMocks."""
    client = AsyncMock(spec=TrelloClient)
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    return client


@pytest.fixture
def sample_board():
    return Board(
        id="board1",
        name="Sprint 42",
        url="https://trello.com/b/1",
        lists=[
            TrelloList(id="list1", name="To Do", card_count=3),
            TrelloList(id="list2", name="Doing", card_count=2),
        ],
    )


@pytest.fixture
def sample_card():
    return Card(
        id="card1",
        name="Fix login timeout",
        desc="The login page times out after 30s",
        due="2026-04-15T12:00:00.000Z",
        closed=False,
        list_name="Doing",
        board_name="Sprint 42",
        labels=[Label(id="lab1", name="bug", color="red")],
        members=[Member(id="mem1", username="james", full_name="James Andrews")],
        comments=[
            Comment(
                id="com1",
                text="Reproduced on staging",
                date="2026-03-28T10:00:00.000Z",
                member_creator=Member(
                    id="mem2", username="sarah", full_name="Sarah Smith"
                ),
            ),
        ],
        url="https://trello.com/c/abc123",
    )


@pytest.fixture
def sample_comment():
    return Comment(
        id="com1",
        text="Great progress!",
        date="2026-04-01T12:00:00.000Z",
        member_creator=Member(
            id="mem1", username="james", full_name="James Andrews"
        ),
    )
