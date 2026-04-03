from __future__ import annotations

from pydantic import BaseModel, Field


class Label(BaseModel):
    id: str
    name: str = ""
    color: str | None = None

    def to_markdown(self) -> str:
        return self.name if self.name else (self.color or "")


class Member(BaseModel):
    id: str
    username: str
    full_name: str = ""

    def to_markdown(self) -> str:
        return f"@{self.username}"


class Comment(BaseModel):
    id: str
    text: str
    date: str
    member_creator: Member

    def to_markdown(self) -> str:
        date_short = self.date[:10]
        return f"**{self.member_creator.to_markdown()}** ({date_short}): {self.text}"


class TrelloList(BaseModel):
    id: str
    name: str
    card_count: int | None = None

    def to_markdown(self) -> str:
        if self.card_count is not None:
            return f"- **{self.name}** ({self.card_count} cards)"
        return f"- **{self.name}**"

    def to_compact_markdown(self) -> str:
        parts = [f"**{self.name}** (id: {self.id})"]
        if self.card_count is not None:
            parts.append(f"{self.card_count} cards")
        return " — ".join(parts)


class Card(BaseModel):
    id: str
    name: str
    desc: str | None = None
    due: str | None = None
    closed: bool = False
    list_name: str | None = None
    board_name: str | None = None
    labels: list[Label] = Field(default_factory=list)
    members: list[Member] = Field(default_factory=list)
    comments: list[Comment] = Field(default_factory=list)
    url: str | None = None

    def to_markdown(self) -> str:
        lines = [f"## {self.name}"]
        if self.list_name:
            lines.append(f"- **List:** {self.list_name}")
        if self.board_name:
            lines.append(f"- **Board:** {self.board_name}")
        if self.due:
            lines.append(f"- **Due:** {self.due[:10]}")
        if self.labels:
            label_str = ", ".join(lbl.to_markdown() for lbl in self.labels)
            lines.append(f"- **Labels:** {label_str}")
        if self.members:
            member_str = ", ".join(m.to_markdown() for m in self.members)
            lines.append(f"- **Members:** {member_str}")
        if self.url:
            lines.append(f"- **URL:** {self.url}")
        if self.desc:
            lines.append(f"\n{self.desc}")
        if self.comments:
            lines.append(f"\n### Comments ({len(self.comments)})")
            for i, c in enumerate(self.comments, 1):
                lines.append(f"{i}. {c.to_markdown()}")
        return "\n".join(lines)

    def to_compact_markdown(self) -> str:
        parts = [f"**{self.name}** (id: {self.id})"]
        if self.due:
            parts.append(f"due {self.due[:10]}")
        if self.labels:
            label_str = ", ".join(lbl.to_markdown() for lbl in self.labels)
            parts.append(f"labels: {label_str}")
        return " — ".join(parts)


class Board(BaseModel):
    id: str
    name: str
    url: str | None = None
    lists: list[TrelloList] = Field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [f"## {self.name}"]
        if self.url:
            lines.append(f"- **URL:** {self.url}")
        if self.lists:
            lines.append(f"\n### Lists ({len(self.lists)})")
            for tl in self.lists:
                lines.append(tl.to_markdown())
        return "\n".join(lines)

    def to_compact_markdown(self) -> str:
        parts = [f"**{self.name}** (id: {self.id})"]
        if self.lists:
            parts.append(f"{len(self.lists)} lists")
        return " — ".join(parts)
