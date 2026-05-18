"""Progress component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHProgress(ttk.Frame):
    """Determinate or indeterminate progress bar with optional label.

    Parameters
    ----------
    mode : "determinate" (default) | "indeterminate"
        When "indeterminate", the bar animates continuously via start()/stop()
        and no label is shown. When "determinate", behaves as before.
    """

    def __init__(
        self,
        master=None,
        label: str | None = None,
        value: int = 0,
        maximum: int = 100,
        mode: str = "determinate",
        **kwargs,
    ):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self._mode = mode

        if mode == "indeterminate":
            self.progress = ttk.Progressbar(
                self, mode="indeterminate", bootstyle="success-striped"
            )
            self.progress.pack(fill="x")
        else:
            if label:
                ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(
                    anchor="w", pady=(0, 4)
                )
            self.progress = ttk.Progressbar(
                self, value=value, maximum=maximum, bootstyle="success"
            )
            self.progress.pack(fill="x")

    def set(self, value: int) -> None:
        """Update the progress value (determinate mode)."""

        self.progress.configure(value=value)

    def start(self, interval: int = 10) -> None:
        """Start the indeterminate animation."""

        self.progress.start(interval)

    def stop(self) -> None:
        """Stop the indeterminate animation."""

        self.progress.stop()
