"""Sidebar navigation component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.navigation.menu_item import IHMenuItem


class IHSidebar(ttk.Frame):
    """Vertical navigation rail for ERP-style desktop apps."""

    def __init__(self, master=None, title: str = "TkInforHard", items: list[tuple[str, object]] | None = None, **kwargs):
        super().__init__(master, padding=16, style="IH.Sidebar.TFrame", **kwargs)
        ttk.Label(self, text=title, style="IH.CardTitle.TLabel").pack(anchor="w", pady=(0, 18))
        self.items: list[IHMenuItem] = []
        for index, item in enumerate(items or []):
            text, command = item
            menu_item = IHMenuItem(self, text=text, command=command, active=index == 0)
            menu_item.pack(fill="x", pady=3)
            self.items.append(menu_item)

