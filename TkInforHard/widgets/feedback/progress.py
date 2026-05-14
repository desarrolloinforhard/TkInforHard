"""Progress component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHProgress(ttk.Frame):
    """Determinate progress bar with optional label."""

    def __init__(self, master=None, label: str | None = None, value: int = 0, maximum: int = 100, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        if label:
            ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(anchor="w", pady=(0, 4))
        self.progress = ttk.Progressbar(self, value=value, maximum=maximum, bootstyle="success")
        self.progress.pack(fill="x")

    def set(self, value: int) -> None:
        """Update the progress value."""

        self.progress.configure(value=value)

