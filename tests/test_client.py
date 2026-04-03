import pytest
from pytest_httpx import HTTPXMock

from trello_mcp.client import TrelloAPIError, TrelloClient


@pytest.fixture
def client():
    return TrelloClient(api_key="test_key", token="test_token")


class TestClientInit:
    def test_base_url(self, client):
        assert str(client._http.base_url) == "https://api.trello.com/1/"

    def test_auth_params(self, client):
        assert client._http.params["key"] == "test_key"
        assert client._http.params["token"] == "test_token"

    @pytest.mark.asyncio
    async def test_context_manager(self):
        client = TrelloClient(api_key="test_key", token="test_token")
        async with client:
            assert not client._http.is_closed
        assert client._http.is_closed


class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_401_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(status_code=401)
        async with client:
            with pytest.raises(TrelloAPIError, match="Authentication failed"):
                await client.get_boards()

    @pytest.mark.asyncio
    async def test_404_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(status_code=404)
        async with client:
            with pytest.raises(TrelloAPIError, match="Not found"):
                await client.get_boards()

    @pytest.mark.asyncio
    async def test_429_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(status_code=429)
        async with client:
            with pytest.raises(TrelloAPIError, match="Rate limited"):
                await client.get_boards()

    @pytest.mark.asyncio
    async def test_500_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(status_code=500)
        async with client:
            with pytest.raises(TrelloAPIError, match="Trello API error"):
                await client.get_boards()

    @pytest.mark.asyncio
    async def test_unhandled_4xx_error(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(status_code=400)
        async with client:
            with pytest.raises(
                TrelloAPIError, match=r"Trello request failed \(HTTP 400\)"
            ):
                await client.get_boards()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status_code", [400, 401, 403, 404, 409, 422, 429, 500, 502, 503]
    )
    async def test_error_messages_never_contain_credentials(
        self, status_code, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(status_code=status_code)
        client = TrelloClient(api_key="test_key", token="test_token")
        async with client:
            with pytest.raises(TrelloAPIError) as exc_info:
                await client.get_boards()
        message = str(exc_info.value)
        assert "test_key" not in message, f"API key leaked in {status_code} error"
        assert "test_token" not in message, f"Token leaked in {status_code} error"


class TestGetBoards:
    @pytest.mark.asyncio
    async def test_returns_boards(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json=[
                {"id": "board1", "name": "Sprint 42", "url": "https://trello.com/b/1"},
                {"id": "board2", "name": "Backlog", "url": "https://trello.com/b/2"},
            ]
        )
        async with client:
            boards = await client.get_boards()
        assert len(boards) == 2
        assert boards[0].name == "Sprint 42"
        assert boards[1].name == "Backlog"

    @pytest.mark.asyncio
    async def test_empty_boards(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=[])
        async with client:
            boards = await client.get_boards()
        assert boards == []


class TestGetBoard:
    @pytest.mark.asyncio
    async def test_returns_board_with_lists(self, client, httpx_mock: HTTPXMock):
        # Responses returned in order: first for board, second for lists
        httpx_mock.add_response(
            json={
                "id": "board1",
                "name": "Sprint 42",
                "url": "https://trello.com/b/1",
            },
        )
        httpx_mock.add_response(
            json=[
                {"id": "list1", "name": "To Do"},
                {"id": "list2", "name": "Doing"},
            ],
        )
        async with client:
            board = await client.get_board("board1")
        assert board.name == "Sprint 42"
        assert len(board.lists) == 2
        assert board.lists[0].name == "To Do"


class TestGetLists:
    @pytest.mark.asyncio
    async def test_returns_lists(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json=[
                {"id": "list1", "name": "To Do"},
                {"id": "list2", "name": "Doing"},
            ]
        )
        async with client:
            lists = await client.get_lists("board1")
        assert len(lists) == 2
        assert lists[0].name == "To Do"


class TestGetCards:
    @pytest.mark.asyncio
    async def test_returns_cards(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json=[
                {
                    "id": "card1",
                    "name": "Fix bug",
                    "desc": "A bug",
                    "due": "2026-04-15T12:00:00.000Z",
                    "closed": False,
                    "labels": [{"id": "lab1", "name": "bug", "color": "red"}],
                },
                {
                    "id": "card2",
                    "name": "Add feature",
                    "desc": "",
                    "due": None,
                    "closed": False,
                    "labels": [],
                },
            ]
        )
        async with client:
            cards = await client.get_cards("list1")
        assert len(cards) == 2
        assert cards[0].name == "Fix bug"
        assert cards[0].labels[0].name == "bug"


class TestGetCard:
    @pytest.mark.asyncio
    async def test_returns_full_card(self, client, httpx_mock: HTTPXMock):
        # Responses returned in order: first for card, second for actions/comments
        httpx_mock.add_response(
            json={
                "id": "card1",
                "name": "Fix bug",
                "desc": "A bug to fix",
                "due": "2026-04-15T12:00:00.000Z",
                "closed": False,
                "labels": [{"id": "lab1", "name": "bug", "color": "red"}],
                "members": [
                    {"id": "mem1", "username": "james", "fullName": "James Andrews"}
                ],
                "url": "https://trello.com/c/abc",
                "board": {"id": "board1", "name": "Sprint 42"},
                "list": {"id": "list1", "name": "Doing"},
            },
        )
        httpx_mock.add_response(
            json=[
                {
                    "id": "act1",
                    "type": "commentCard",
                    "date": "2026-03-28T10:00:00.000Z",
                    "data": {"text": "Reproduced on staging"},
                    "memberCreator": {
                        "id": "mem2",
                        "username": "sarah",
                        "fullName": "Sarah Smith",
                    },
                }
            ],
        )
        async with client:
            card = await client.get_card("card1")
        assert card.name == "Fix bug"
        assert card.list_name == "Doing"
        assert card.board_name == "Sprint 42"
        assert len(card.comments) == 1
        assert card.comments[0].text == "Reproduced on staging"


class TestCreateCard:
    @pytest.mark.asyncio
    async def test_create_minimal(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "id": "newcard1",
                "name": "New task",
                "desc": "",
                "due": None,
                "closed": False,
                "labels": [],
                "url": "https://trello.com/c/new",
            }
        )
        async with client:
            card = await client.create_card(list_id="list1", name="New task")
        assert card.name == "New task"

    @pytest.mark.asyncio
    async def test_create_with_options(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "id": "newcard2",
                "name": "Detailed task",
                "desc": "Some details",
                "due": "2026-05-01T00:00:00.000Z",
                "closed": False,
                "labels": [],
                "url": "https://trello.com/c/new2",
            }
        )
        async with client:
            card = await client.create_card(
                list_id="list1",
                name="Detailed task",
                desc="Some details",
                due="2026-05-01",
            )
        assert card.name == "Detailed task"
        assert card.desc == "Some details"


class TestUpdateCard:
    @pytest.mark.asyncio
    async def test_update_name(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "id": "card1",
                "name": "Updated name",
                "desc": "",
                "due": None,
                "closed": False,
                "labels": [],
                "url": "https://trello.com/c/abc",
            }
        )
        async with client:
            card = await client.update_card("card1", name="Updated name")
        assert card.name == "Updated name"

    @pytest.mark.asyncio
    async def test_move_card(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "id": "card1",
                "name": "Task",
                "desc": "",
                "due": None,
                "closed": False,
                "labels": [],
                "url": "https://trello.com/c/abc",
            }
        )
        async with client:
            card = await client.update_card("card1", list_id="list2")
        assert card.name == "Task"


class TestArchiveCard:
    @pytest.mark.asyncio
    async def test_archive(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "id": "card1",
                "name": "Archived task",
                "desc": "",
                "due": None,
                "closed": True,
                "labels": [],
                "url": "https://trello.com/c/abc",
            }
        )
        async with client:
            card = await client.archive_card("card1")
        assert card.closed is True


class TestAddComment:
    @pytest.mark.asyncio
    async def test_add_comment(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "id": "act1",
                "type": "commentCard",
                "date": "2026-04-01T12:00:00.000Z",
                "data": {"text": "Great progress!"},
                "memberCreator": {
                    "id": "mem1",
                    "username": "james",
                    "fullName": "James Andrews",
                },
            }
        )
        async with client:
            comment = await client.add_comment("card1", "Great progress!")
        assert comment.text == "Great progress!"


class TestSearchCards:
    @pytest.mark.asyncio
    async def test_search(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={
                "cards": [
                    {
                        "id": "card1",
                        "name": "Fix login",
                        "desc": "",
                        "due": None,
                        "closed": False,
                        "labels": [],
                        "board": {"id": "board1", "name": "Sprint 42"},
                        "list": {"id": "list1", "name": "Doing"},
                    }
                ]
            }
        )
        async with client:
            cards = await client.search_cards("login")
        assert len(cards) == 1
        assert cards[0].name == "Fix login"
        assert cards[0].board_name == "Sprint 42"

    @pytest.mark.asyncio
    async def test_search_scoped_to_board(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"cards": []})
        async with client:
            cards = await client.search_cards("login", board_id="board1")
        assert cards == []
        request = httpx_mock.get_request()
        assert "board1" in str(request.url)  # pyrefly: ignore [missing-attribute]

    @pytest.mark.asyncio
    async def test_search_no_results(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"cards": []})
        async with client:
            cards = await client.search_cards("nonexistent")
        assert cards == []
