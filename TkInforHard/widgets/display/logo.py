"""Logo component."""

from pathlib import Path

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHLogo(ttk.Label):
    """Logo label that can later be upgraded to render image assets."""

    def __init__(self, master=None, text: str = "Inforhard", image_path: str | Path | None = None, **kwargs):
        super().__init__(master, text=text, style="IH.CardTitle.TLabel", **kwargs)
        self.image_path = Path(image_path) if image_path else None

