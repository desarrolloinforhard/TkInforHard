"""Information card component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.cards.card import IHCard


class IHInfoCard(IHCard):
    """Card for short explanatory content or records."""

    def __init__(
        self,
        master=None,
        title: str = "",
        body: str = "",
        action=None,
        variant: str = "default",
        **kwargs,
    ):
        super().__init__(master, title=title, padding=18, variant=variant, **kwargs)
        ttk.Label(self.content, text=body, style="IH.CardMuted.TLabel", wraplength=360, justify="left").pack(anchor="w", pady=(8, 0))
        if action:
            action.pack(in_=self.content, anchor="e", pady=(12, 0))
