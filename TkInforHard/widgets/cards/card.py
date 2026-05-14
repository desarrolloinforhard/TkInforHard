"""Card container."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHCard(ttk.Frame):
    """Surface container for grouping related content."""

    def __init__(self, master=None, title: str | None = None, subtitle: str | None = None, padding: int = 16, **kwargs):
        kwargs.setdefault("style", "IH.Card.TFrame")
        super().__init__(master, padding=padding, **kwargs)
        self.title_text = title
        self.subtitle_text = subtitle
        if title:
            ttk.Label(self, text=title, style="IH.CardTitle.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(self, text=subtitle, style="IH.CardMuted.TLabel").pack(anchor="w", pady=(2, 10))

