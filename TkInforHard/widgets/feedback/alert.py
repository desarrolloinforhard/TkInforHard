"""Alert component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHAlert(ttk.Frame):
    """Inline feedback message with a semantic variant."""

    def __init__(self, master=None, title: str = "", message: str = "", variant: str = "info", **kwargs):
        super().__init__(master, padding=12, style="IH.Card.TFrame", **kwargs)
        self.variant = variant
        if title:
            ttk.Label(self, text=title, style="IH.CardTitle.TLabel").pack(anchor="w")
        ttk.Label(self, text=message, style="IH.CardMuted.TLabel", wraplength=520).pack(anchor="w", pady=(4, 0))

