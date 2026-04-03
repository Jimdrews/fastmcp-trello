import pytest

from trello_mcp.models import Board, Card, Comment, Label, Member, TrelloList


class TestLabel:
    def test_parse(self):
        label = Label(id="lab1", name="bug", color="red")
        assert label.id == "lab1"
        assert label.name == "bug"
        assert label.color == "red"

    def test_parse_no_color(self):
        label = Label(id="lab1", name="priority")
        assert label.color is None

    def test_to_markdown(self):
        label = Label(id="lab1", name="bug", color="red")
        assert label.to_markdown() == "bug"

    def test_to_markdown_no_name(self):
        label = Label(id="lab1", name="", color="red")
        assert label.to_markdown() == "red"


class TestMember:
    def test_parse(self):
        member = Member(id="mem1", username="james", full_name="James Andrews")
        assert member.username == "james"
        assert member.full_name == "James Andrews"

    def test_to_markdown(self):
        member = Member(id="mem1", username="james", full_name="James Andrews")
        assert member.to_markdown() == "@james"


class TestComment:
    def test_parse(self):
        comment = Comment(
            id="com1",
            text="Fixed the bug",
            date="2026-03-28T10:00:00.000Z",
            member_creator=Member(
                id="mem1", username="james", full_name="James Andrews"
            ),
        )
        assert comment.text == "Fixed the bug"

    def test_to_markdown(self):
        comment = Comment(
            id="com1",
            text="Fixed the bug",
            date="2026-03-28T10:00:00.000Z",
            member_creator=Member(
                id="mem1", username="james", full_name="James Andrews"
            ),
        )
        md = comment.to_markdown()
        assert "@james" in md
        assert "Fixed the bug" in md
        assert "2026-03-28" in md


class TestTrelloList:
    def test_parse(self):
        tl = TrelloList(id="list1", name="To Do", card_count=5)
        assert tl.name == "To Do"

    def test_to_markdown(self):
        tl = TrelloList(id="list1", name="To Do", card_count=5)
        md = tl.to_markdown()
        assert "To Do" in md
        assert "5" in md

    def test_to_markdown_no_card_count(self):
        tl = TrelloList(id="list1", name="To Do")
        md = tl.to_markdown()
        assert "To Do" in md


class TestCard:
    @pytest.fixture
    def full_card(self):
        return Card(
            id="card1",
            name="Fix login timeout",
            desc="The login page times out after 30s",
            due="2026-04-15T12:00:00.000Z",
            closed=False,
            list_name="Doing",
            board_name="Sprint 42",
            labels=[
                Label(id="lab1", name="bug", color="red"),
                Label(id="lab2", name="urgent", color="orange"),
            ],
            members=[
                Member(id="mem1", username="james", full_name="James Andrews"),
            ],
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
    def minimal_card(self):
        return Card(id="card2", name="Quick task", closed=False)

    def test_parse_full(self, full_card):
        assert full_card.name == "Fix login timeout"
        assert full_card.list_name == "Doing"
        assert len(full_card.labels) == 2
        assert len(full_card.members) == 1
        assert len(full_card.comments) == 1

    def test_parse_minimal(self, minimal_card):
        assert minimal_card.name == "Quick task"
        assert minimal_card.desc is None
        assert minimal_card.labels == []
        assert minimal_card.members == []
        assert minimal_card.comments == []

    def test_to_markdown_full(self, full_card):
        md = full_card.to_markdown()
        assert "## Fix login timeout" in md
        assert "Doing" in md
        assert "Sprint 42" in md
        assert "2026-04-15" in md
        assert "bug" in md
        assert "urgent" in md
        assert "@james" in md
        assert "login page times out" in md
        assert "Reproduced on staging" in md

    def test_to_markdown_minimal(self, minimal_card):
        md = minimal_card.to_markdown()
        assert "## Quick task" in md
        # Should not have empty sections
        assert "Labels" not in md or "None" not in md

    def test_compact_markdown(self, full_card):
        md = full_card.to_compact_markdown()
        # Compact should be a single line with key info
        assert "Fix login timeout" in md
        assert "card1" in md


class TestBoard:
    @pytest.fixture
    def board(self):
        return Board(
            id="board1",
            name="Sprint 42",
            url="https://trello.com/b/xyz789",
            lists=[
                TrelloList(id="list1", name="To Do", card_count=3),
                TrelloList(id="list2", name="Doing", card_count=2),
                TrelloList(id="list3", name="Done", card_count=7),
            ],
        )

    @pytest.fixture
    def empty_board(self):
        return Board(id="board2", name="Empty Board", url="https://trello.com/b/empty")

    def test_parse(self, board):
        assert board.name == "Sprint 42"
        assert len(board.lists) == 3

    def test_to_markdown(self, board):
        md = board.to_markdown()
        assert "## Sprint 42" in md
        assert "To Do" in md
        assert "Doing" in md
        assert "Done" in md

    def test_to_markdown_empty(self, empty_board):
        md = empty_board.to_markdown()
        assert "Empty Board" in md

    def test_compact_markdown(self, board):
        md = board.to_compact_markdown()
        assert "Sprint 42" in md
        assert "board1" in md
