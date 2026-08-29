from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Markdown, Static


class UserTurn(Static):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def on_mount(self) -> None:
        self.update(f"[$primary bold]❯[/] {self.text}")


class SystemTurn(Static):
    def __init__(self, markup: str) -> None:
        super().__init__()
        self.markup = markup

    def on_mount(self) -> None:
        self.update(self.markup)


class AgentTurn(Vertical):
    def __init__(self) -> None:
        super().__init__()
        self.body = Markdown()
        self._cursor = Static("▋", classes="cursor")
        self._blink = None

    def compose(self) -> ComposeResult:
        yield Static("[$secondary bold]▌ pantokrator[/]", classes="speaker")
        yield self.body
        yield self._cursor

    def on_mount(self) -> None:
        visible = True

        def blink() -> None:
            nonlocal visible
            visible = not visible
            self._cursor.update("▋" if visible else " ")

        self._blink = self.set_interval(0.5, blink)

    def finish(self, note: str = "") -> None:
        if self._blink is not None:
            self._blink.stop()
            self._blink = None
        self._cursor.update(note)
        self._cursor.set_class(bool(note), "note")
        self._cursor.display = bool(note)
