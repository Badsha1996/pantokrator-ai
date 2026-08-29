from textual.theme import Theme
PANTOKRATOR_THEME = Theme(
    name="pantokrator",
    primary="#f0b45f",
    secondary="#6fd6e2",
    accent="#b48ef5",
    foreground="#d3d8e2",
    background="#0a0c10",
    surface="#11141a",
    panel="#161a22",
    success="#7ee787",
    warning="#f0b45f",
    error="#ff7b72",
    dark=True,
)

PHASE = "STILL IN WORKS"

HELP = """\
[$secondary bold]/help[/]     this text
[$secondary bold]/clear[/]    wipe the scrollback
[$secondary bold]/history[/]  everything you've typed this session
[$secondary bold]/quit[/]     leave

[$text-muted]↑ ↓ recall previous prompts · esc interrupts a reply[/]"""

BANNER = """\
[$primary bold]P A N T O K R A T O R[/]
[$text-muted]A GROWING BRAIN INSIDE COMPUTER[/]

[$text-muted]Type below.[/] [$secondary]/help[/] [$text-muted]for commands.[/]"""
