"""Sidebar navigation component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.navigation.menu_item import IHMenuItem


class IHSidebar(ttk.Frame):
    """Vertical navigation rail for ERP-style desktop apps."""

    def __init__(self, master=None, title: str = "TkInforHard", items: list[tuple[str, object]] | None = None, **kwargs):
        super().__init__(master, padding=(6, 14), style="IH.Sidebar.TFrame", **kwargs)
        ttk.Label(self, text=title, style="IH.SidebarTitle.TLabel").pack(anchor="w", padx=2, pady=(0, 18))
        self.items: list[IHMenuItem] = []
        for index, item in enumerate(items or []):
            text, command = item
            menu_item = IHMenuItem(self, text=text, command=lambda idx=index, cb=command: self._activate(idx, cb), active=index == 0)
            menu_item.pack(fill="x", pady=(0, 4))
            self.items.append(menu_item)

    def _activate(self, index: int, command) -> None:
        for item_index, item in enumerate(self.items):
            item.set_active(item_index == index)
        if command:
            command()
