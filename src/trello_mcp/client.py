from __future__ import annotations

from typing import Any

import httpx

from trello_mcp.models import (
    Attachment,
    Board,
    Card,
    Comment,
    Label,
    Member,
    TrelloList,
)


class TrelloAPIError(Exception):
    pass


_ERROR_MESSAGES = {
    401: "Authentication failed. Check your TRELLO_API_KEY and TRELLO_TOKEN.",
    404: "Not found. The resource may have been deleted or the ID is incorrect.",
    429: "Rate limited by Trello. Please wait a moment and try again.",
}


class TrelloClient:
    def __init__(self, api_key: str, token: str) -> None:
        self._http = httpx.AsyncClient(
            base_url="https://api.trello.com/1/",
            params={"key": api_key, "token": token},
        )

    async def __aenter__(self) -> TrelloClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self._http.aclose()

    async def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        response = await self._http.request(method, path, **kwargs)
        if response.status_code in _ERROR_MESSAGES:
            raise TrelloAPIError(_ERROR_MESSAGES[response.status_code])
        if response.status_code >= 500:
            raise TrelloAPIError("Trello API error. Please try again.")
        if response.status_code >= 400:
            raise TrelloAPIError(
                f"Trello request failed (HTTP {response.status_code})."
            )
        return response

    # --- Boards ---

    async def get_boards(self) -> list[Board]:
        resp = await self._request(
            "GET", "members/me/boards", params={"filter": "open"}
        )
        return [
            Board(id=b["id"], name=b["name"], url=b.get("url")) for b in resp.json()
        ]

    async def get_board(self, board_id: str) -> Board:
        resp = await self._request("GET", f"boards/{board_id}")
        data = resp.json()
        lists = await self.get_lists(board_id)
        return Board(
            id=data["id"],
            name=data["name"],
            url=data.get("url"),
            lists=lists,
        )

    async def create_board(
        self, name: str, desc: str | None = None, default_lists: bool = True
    ) -> Board:
        default = str(default_lists).lower()
        data: dict[str, str] = {"name": name, "defaultLists": default}
        if desc is not None:
            data["desc"] = desc
        resp = await self._request("POST", "boards", data=data)
        d = resp.json()
        return Board(id=d["id"], name=d["name"], url=d.get("url"))

    async def update_board(
        self, board_id: str, name: str | None = None, desc: str | None = None
    ) -> Board:
        data: dict[str, str] = {}
        if name is not None:
            data["name"] = name
        if desc is not None:
            data["desc"] = desc
        resp = await self._request("PUT", f"boards/{board_id}", data=data)
        d = resp.json()
        return Board(id=d["id"], name=d["name"], url=d.get("url"))

    async def close_board(self, board_id: str) -> Board:
        resp = await self._request("PUT", f"boards/{board_id}", data={"closed": "true"})
        d = resp.json()
        return Board(id=d["id"], name=d["name"], url=d.get("url"))

    async def get_lists(self, board_id: str) -> list[TrelloList]:
        resp = await self._request(
            "GET", f"boards/{board_id}/lists", params={"filter": "open"}
        )
        return [TrelloList(id=item["id"], name=item["name"]) for item in resp.json()]

    # --- Lists ---

    async def create_list(
        self, board_id: str, name: str, position: str | None = None
    ) -> TrelloList:
        data: dict[str, str] = {"idBoard": board_id, "name": name}
        if position is not None:
            data["pos"] = position
        resp = await self._request("POST", "lists", data=data)
        item = resp.json()
        return TrelloList(id=item["id"], name=item["name"])

    async def update_list(self, list_id: str, name: str) -> TrelloList:
        resp = await self._request("PUT", f"lists/{list_id}", data={"name": name})
        item = resp.json()
        return TrelloList(id=item["id"], name=item["name"])

    async def archive_list(self, list_id: str) -> TrelloList:
        resp = await self._request(
            "PUT", f"lists/{list_id}/closed", data={"value": "true"}
        )
        item = resp.json()
        return TrelloList(id=item["id"], name=item["name"])

    async def move_list(self, list_id: str, position: str) -> TrelloList:
        resp = await self._request("PUT", f"lists/{list_id}", data={"pos": position})
        item = resp.json()
        return TrelloList(id=item["id"], name=item["name"])

    # --- Cards ---

    async def get_cards(self, list_id: str) -> list[Card]:
        resp = await self._request("GET", f"lists/{list_id}/cards")
        return [self._parse_card_summary(c) for c in resp.json()]

    async def get_card(self, card_id: str) -> Card:
        resp = await self._request(
            "GET",
            f"cards/{card_id}",
            params={"members": "true", "board": "true", "list": "true"},
        )
        data = resp.json()

        comments_resp = await self._request(
            "GET",
            f"cards/{card_id}/actions",
            params={"filter": "commentCard"},
        )
        comments = [
            Comment(
                id=a["id"],
                text=a["data"]["text"],
                date=a["date"],
                member_creator=Member(
                    id=a["memberCreator"]["id"],
                    username=a["memberCreator"]["username"],
                    full_name=a["memberCreator"].get("fullName", ""),
                ),
            )
            for a in comments_resp.json()
        ]

        members = [
            Member(
                id=m["id"],
                username=m["username"],
                full_name=m.get("fullName", ""),
            )
            for m in data.get("members", [])
        ]

        labels = [
            Label(id=lbl["id"], name=lbl.get("name", ""), color=lbl.get("color"))
            for lbl in data.get("labels", [])
        ]

        return Card(
            id=data["id"],
            name=data["name"],
            desc=data.get("desc") or None,
            due=data.get("due"),
            closed=data.get("closed", False),
            list_name=data.get("list", {}).get("name"),
            board_name=data.get("board", {}).get("name"),
            labels=labels,
            members=members,
            comments=comments,
            url=data.get("url"),
        )

    async def create_card(
        self,
        list_id: str,
        name: str,
        desc: str | None = None,
        due: str | None = None,
    ) -> Card:
        data: dict[str, str] = {"idList": list_id, "name": name}
        if desc is not None:
            data["desc"] = desc
        if due is not None:
            data["due"] = due
        resp = await self._request("POST", "cards", data=data)
        return self._parse_card_summary(resp.json())

    async def update_card(
        self,
        card_id: str,
        name: str | None = None,
        desc: str | None = None,
        due: str | None = None,
        list_id: str | None = None,
    ) -> Card:
        data: dict[str, str] = {}
        if name is not None:
            data["name"] = name
        if desc is not None:
            data["desc"] = desc
        if due is not None:
            data["due"] = due
        if list_id is not None:
            data["idList"] = list_id
        resp = await self._request("PUT", f"cards/{card_id}", data=data)
        return self._parse_card_summary(resp.json())

    async def archive_card(self, card_id: str) -> Card:
        resp = await self._request("PUT", f"cards/{card_id}", data={"closed": "true"})
        return self._parse_card_summary(resp.json())

    # --- Labels ---

    async def get_labels(self, board_id: str) -> list[Label]:
        resp = await self._request("GET", f"boards/{board_id}/labels")
        return [
            Label(id=lbl["id"], name=lbl.get("name", ""), color=lbl.get("color"))
            for lbl in resp.json()
        ]

    async def create_label(
        self, board_id: str, name: str, color: str | None = None
    ) -> Label:
        data: dict[str, str] = {"name": name}
        if color is not None:
            data["color"] = color
        resp = await self._request("POST", f"boards/{board_id}/labels", data=data)
        lbl = resp.json()
        return Label(id=lbl["id"], name=lbl.get("name", ""), color=lbl.get("color"))

    async def delete_label(self, label_id: str) -> None:
        await self._request("DELETE", f"labels/{label_id}")

    async def add_label_to_card(self, card_id: str, label_id: str) -> None:
        await self._request(
            "POST", f"cards/{card_id}/idLabels", data={"value": label_id}
        )

    async def remove_label_from_card(self, card_id: str, label_id: str) -> None:
        await self._request("DELETE", f"cards/{card_id}/idLabels/{label_id}")

    # --- Attachments ---

    async def get_attachments(self, card_id: str) -> list[Attachment]:
        resp = await self._request("GET", f"cards/{card_id}/attachments")
        return [
            Attachment(
                id=a["id"],
                name=a["name"],
                url=a["url"],
                date=a["date"],
                bytes=a.get("bytes"),
            )
            for a in resp.json()
        ]

    async def add_attachment(
        self, card_id: str, url: str, name: str | None = None
    ) -> Attachment:
        data: dict[str, str] = {"url": url}
        if name is not None:
            data["name"] = name
        resp = await self._request("POST", f"cards/{card_id}/attachments", data=data)
        a = resp.json()
        return Attachment(
            id=a["id"],
            name=a["name"],
            url=a["url"],
            date=a["date"],
            bytes=a.get("bytes"),
        )

    async def delete_attachment(self, card_id: str, attachment_id: str) -> None:
        await self._request("DELETE", f"cards/{card_id}/attachments/{attachment_id}")

    # --- Comments ---

    async def add_comment(self, card_id: str, text: str) -> Comment:
        resp = await self._request(
            "POST", f"cards/{card_id}/actions/comments", data={"text": text}
        )
        data = resp.json()
        return Comment(
            id=data["id"],
            text=data["data"]["text"],
            date=data["date"],
            member_creator=Member(
                id=data["memberCreator"]["id"],
                username=data["memberCreator"]["username"],
                full_name=data["memberCreator"].get("fullName", ""),
            ),
        )

    # --- Search ---

    async def search_cards(self, query: str, board_id: str | None = None) -> list[Card]:
        params: dict[str, str] = {"query": query, "modelTypes": "cards"}
        if board_id:
            params["idBoards"] = board_id
        resp = await self._request("GET", "search", params=params)
        cards_data = resp.json().get("cards", [])
        return [
            Card(
                id=c["id"],
                name=c["name"],
                desc=c.get("desc") or None,
                due=c.get("due"),
                closed=c.get("closed", False),
                labels=[
                    Label(
                        id=lbl["id"],
                        name=lbl.get("name", ""),
                        color=lbl.get("color"),
                    )
                    for lbl in c.get("labels", [])
                ],
                board_name=c.get("board", {}).get("name"),
                list_name=c.get("list", {}).get("name"),
            )
            for c in cards_data
        ]

    # --- Helpers ---

    def _parse_card_summary(self, data: dict) -> Card:
        return Card(
            id=data["id"],
            name=data["name"],
            desc=data.get("desc") or None,
            due=data.get("due"),
            closed=data.get("closed", False),
            labels=[
                Label(id=lbl["id"], name=lbl.get("name", ""), color=lbl.get("color"))
                for lbl in data.get("labels", [])
            ],
            url=data.get("url"),
        )
