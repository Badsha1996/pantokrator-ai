from __future__ import annotations

import asyncio
import contextlib

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import reactive

from textual.widgets import Footer, Input, Markdown, Static

from .chat import AgentTurn, SystemTurn, UserTurn
from .engine import EchoEngine, Engine
from .theme.theme import BANNER, HELP, PANTOKRATOR_THEME, PHASE



class PromptInput(Input):
    BINDINGS = [
        Binding("up", "recall(-1)", "history", show=False),
        Binding("down", "recall(1)", "history", show=False),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.history: list[str] = []
        self._cursor_in_history = 0

    def remember(self, text: str) -> None:
        if text and (not self.history or self.history[-1] != text): self.history.append(text)
        self._cursor_in_history = len(self.history)

    def action_recall(self, offset: int) -> None:
        if not self.history: return

        position = self._cursor_in_history + offset
        self._cursor_in_history = max(0, min(position, len(self.history)))
        if self._cursor_in_history == len(self.history):
            self.value = ""
        else:
            self.value = self.history[self._cursor_in_history]
        self.action_end()


class PantokratorApp(App):
    CSS_PATH = "tui.tcss"
    TITLE = "pantokrator"
    BINDINGS = [
        Binding("ctrl+q", "quit", "quit"),
        Binding("ctrl+l", "clear", "clear"),
        Binding("escape", "interrupt", "interrupt"),
    ]

    busy: reactive[bool] = reactive(False)

    def __init__(self, engine: Engine | None = None) -> None:
        super().__init__()
        self.engine: Engine = engine or EchoEngine()

    def compose(self) -> ComposeResult:
        with Horizontal(id="banner"):
            yield Static("[$primary bold]◈[/] [b]pantokrator[/]", id="wordmark")
            yield Static(id="status")

        yield VerticalScroll(Static(BANNER, classes="hero"), id="transcript")

        with Horizontal(id="prompt-bar"):
            yield Static("[$primary bold]❯[/]", id="caret")
            yield PromptInput(placeholder="ask pantokrator…", id="prompt")

        yield Footer()

    def on_mount(self) -> None:
        self.register_theme(PANTOKRATOR_THEME)
        self.theme = "pantokrator"
        self.query_one("#prompt", PromptInput).focus()
        self.watch_busy(False)

    @property
    def transcript(self) -> VerticalScroll: return self.query_one("#transcript", VerticalScroll)

    def watch_busy(self, busy: bool) -> None:
        dot = "[$warning]●[/] working" if busy else "[$success]●[/] idle"
        with contextlib.suppress(Exception):
            self.query_one("#status", Static).update(
                f"{dot}  [$text-muted]·[/]  local:{self.engine.name}  "
                f"[$text-muted]·[/]  {PHASE}"
            )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        prompt = event.value.strip()
        event.input.value = ""
        if not prompt:
            return

        field = self.query_one("#prompt", PromptInput)
        field.remember(prompt)
        await self.say(UserTurn(prompt))

        if prompt.startswith("/"):
            await self.run_command(prompt)
        elif self.busy:
            await self.say(
                SystemTurn("[$warning]still answering — press esc to interrupt.[/]")
            )
        else:
            self.reply(prompt)

    async def say(self, widget) -> None:
        await self.transcript.mount(widget)
        self.transcript.scroll_end(animate=False)

    async def run_command(self, line: str) -> None:
        command = line.split()[0].lower()
        if command == "/help":
            await self.say(SystemTurn(HELP))
        elif command == "/clear":
            await self.action_clear()
        elif command == "/history":
            history = self.query_one("#prompt", PromptInput).history
            listing = "\n".join(f"[$text-muted]{i:>3}[/]  {h}" for i, h in enumerate(history, 1))
            await self.say(SystemTurn(listing or "[$text-muted]nothing yet.[/]"))
        elif command in ("/quit", "/exit"):
            self.exit()
        else:
            await self.say(SystemTurn(f"[$error]unknown command:[/] {command}"))

    @work(exclusive=True, group="reply")
    async def reply(self, prompt: str) -> None:
        turn = AgentTurn()
        await self.say(turn)
        self.busy = True
        self.transcript.anchor()

        stream = Markdown.get_stream(turn.body)
        note = ""
        try:
            async for fragment in self.engine.stream(prompt):
                await stream.write(fragment)
        except asyncio.CancelledError:
            note = "[$warning]interrupted.[/]"
        finally:
            with contextlib.suppress(Exception, asyncio.CancelledError):
                await stream.stop()
            turn.finish(note)
            self.busy = False
            self.transcript.scroll_end(animate=False)

    def action_interrupt(self) -> None:
        if self.busy: self.workers.cancel_group(self, "reply")

    async def action_clear(self) -> None:
        await self.transcript.remove_children()
        await self.transcript.mount(Static(BANNER, classes="hero"))
