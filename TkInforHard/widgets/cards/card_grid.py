"""Card grid layout helper."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHCardGrid(ttk.Frame):
    """Grid helper for arranging cards with consistent spacing."""

    def __init__(self, master=None, columns: int = 3, gap: int = 12, **kwargs):
        super().__init__(master, style="IH.TFrame", **kwargs)
        self.columns = max(1, int(columns))
        self.gap = gap
        for column in range(self.columns):
            self.columnconfigure(column, weight=1, uniform="ih_card_grid")

    def add(self, child, index: int | None = None):
        """Place a child in the next or requested grid slot."""

        if index is None:
            index = len(self.grid_slaves())
        row = index // self.columns
        column = index % self.columns
        child.grid(row=row, column=column, sticky="nsew", padx=self.gap // 2, pady=self.gap // 2)
        return child
