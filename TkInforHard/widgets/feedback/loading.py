"""Loading indicator component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHLoading(ttk.Frame):
    """Indeterminate progress indicator for async operations."""

    def __init__(self, master=None, text: str = "Cargando...", **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        ttk.Label(self, text=text, style="IH.Surface.TLabel").pack(anchor="w")
        self.progress = ttk.Progressbar(self, mode="indeterminate", bootstyle="success-striped")
        self.progress.pack(fill="x", pady=(8, 0))

    def start(self, interval: int = 10) -> None:
        """Start the loading animation."""

        self.progress.start(interval)

    def stop(self) -> None:
        """Stop the loading animation."""

        self.progress.stop()

