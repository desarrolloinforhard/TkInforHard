"""Combobox component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHCombobox(ttk.Frame):
    """Labeled combobox component."""

    def __init__(self, master=None, label: str | None = None, values: list[str] | tuple[str, ...] = (), **kwargs):
        super().__init__(master, style="IH.Surface.TFrame")
        if label:
            ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(anchor="w", pady=(0, 4))
        self.combobox = ttk.Combobox(self, values=values, style="IH.TCombobox", **kwargs)
        self.combobox.pack(fill="x")

    def get(self) -> str:
        """Return the selected value."""

        return self.combobox.get()

