"""Table component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHTable(ttk.Frame):
    """Reusable Treeview table with a small data-loading API."""

    def __init__(self, master=None, columns: list[str] | tuple[str, ...] = (), rows: list[tuple] | None = None, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="IH.Treeview")
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=140, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.load(rows or [])

    def load(self, rows: list[tuple]) -> None:
        """Replace table rows."""

        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", "end", values=row)

