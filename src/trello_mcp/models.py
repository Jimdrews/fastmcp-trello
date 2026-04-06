from __future__ import annotations

from pydantic import BaseModel, Field


class TrelloModel(BaseModel):
    id: str

    def to_markdown(self) -> str:
        parts = []
        for name, value in self:
            if name == "id" or value is None:
                continue
            if isinstance(value, bool) and not value:
                continue
            if isinstance(value, list):
                if not value:
                    continue
                if hasattr(value[0], "to_markdown"):
                    value = ", ".join(v.to_markdown() for v in value)
                else:
                    value = ", ".join(str(v) for v in value)
            parts.append(f"**{name}:** {value}")
        return f"(id: {self.id}) " + " | ".join(parts) if parts else f"(id: {self.id})"


class Label(TrelloModel):
    name: str = ""
    color: str | None = None


class Member(TrelloModel):
    username: str
    full_name: str = ""

    def to_markdown(self) -> str:
        return f"@{self.username}"


class Comment(TrelloModel):
    text: str
    date: str
    member_creator: Member

    def to_markdown(self) -> str:
        date_short = self.date[:10]
        return f"**{self.member_creator.to_markdown()}** ({date_short}): {self.text}"


class Attachment(TrelloModel):
    name: str
    url: str
    date: str
    bytes: int | None = None


class TrelloList(TrelloModel):
    name: str
    card_count: int | None = None


class Card(TrelloModel):
    name: str
    desc: str | None = None
    due: str | None = None
    pos: float | None = None
    closed: bool = False
    list_name: str | None = None
    board_name: str | None = None
    labels: list[Label] = Field(default_factory=list)
    members: list[Member] = Field(default_factory=list)
    comments: list[Comment] = Field(default_factory=list)
    url: str | None = None

    def to_markdown(self) -> str:
        lines = [f"## {self.name} (id: {self.id})"]
        if self.list_name:
            lines.append(f"- **List:** {self.list_name}")
        if self.board_name:
            lines.append(f"- **Board:** {self.board_name}")
        if self.due:
            lines.append(f"- **Due:** {self.due[:10]}")
        if self.pos is not None:
            lines.append(f"- **Position:** {self.pos}")
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


class Board(TrelloModel):
    name: str
    url: str | None = None
    lists: list[TrelloList] = Field(default_factory=list)
