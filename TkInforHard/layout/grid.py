"""Grid layout helper."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHGrid(ttk.Frame):
    """Responsive-ish grid helper based on ttk grid geometry."""

    def __init__(self, master=None, columns: int = 3, gap: int = 12, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self.columns = columns
        self.gap = gap
        for index in range(columns):
            self.columnconfigure(index, weight=1)

    def add(self, child, index: int):
        """Place a child at a calculated row/column position."""

        row = index // self.columns
        column = index % self.columns
        child.grid(row=row, column=column, sticky="nsew", padx=self.gap // 2, pady=self.gap // 2)
        return child

