"""Animated drawer menu component."""

from __future__ import annotations

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.buttons.button import IHButton
from TkInforHard.widgets.navigation.menu_item import IHMenuItem


class IHDrawerMenu(ttk.Frame):
    """Animated sliding menu that can host navigation items and custom widgets."""

    def __init__(
        self,
        master=None,
        title: str | None = None,
        side: str = "right",
        width: int = 300,
        animation_step: int = 24,
        animation_delay: int = 10,
        **kwargs,
    ):
        if side not in {"left", "right"}:
            raise ValueError("side must be 'left' or 'right'")
        super().__init__(master, width=width, style="IH.Sidebar.TFrame", **kwargs)
        self.side = side
        self.drawer_width = width
        self.animation_step = animation_step
        self.animation_delay = animation_delay
        self._is_open = False
        self._animating = False
        self._animation_job = None
        self._items: list[IHMenuItem] = []
        self.pack_propagate(False)

        self.header = ttk.Frame(self, padding=(16, 16, 16, 8), style="IH.Sidebar.TFrame")
        self.header.pack(fill="x")
        if title:
            ttk.Label(self.header, text=title, style="IH.SidebarTitle.TLabel").pack(anchor="w")

        self.content = ttk.Frame(self, padding=(12, 8, 12, 12), style="IH.Sidebar.TFrame")
        self.content.pack(fill="both", expand=True)

        self.after_idle(self._place_initial)
        self.master.bind("<Configure>", self._on_parent_configure, add="+")

    @property
    def is_open(self) -> bool:
        """Return whether the drawer is currently open."""

        return self._is_open

    def add_item(self, text: str, command=None, icon=None, active: bool = False) -> IHMenuItem:
        """Add a navigation item to the drawer and return it."""

        item = IHMenuItem(
            self.content,
            text=text,
            icon=icon,
            active=active,
            command=lambda target=None: self._activate_item(item, command),
            width=max(self.drawer_width - 24, IHMenuItem.WIDTH),
        )
        item.pack(fill="x", pady=(0, 4))
        self._items.append(item)
        return item

    def add_widget(self, widget, **pack_options):
        """Pack an arbitrary widget inside the drawer content frame."""

        defaults = {"fill": "x", "pady": (0, 8)}
        defaults.update(pack_options)
        widget.pack(in_=self.content, **defaults)
        return widget

    def clear(self) -> None:
        """Destroy all content widgets currently hosted by the drawer."""

        for child in self.content.winfo_children():
            child.destroy()
        self._items.clear()

    def create_toggle_button(self, master=None, text: str = "Menu", **kwargs) -> IHButton:
        """Create a button already wired to toggle this drawer."""

        return IHButton(master or self.master, text=text, command=self.toggle, **kwargs)

    def open(self) -> None:
        """Open the drawer with a sliding animation."""

        self._is_open = True
        self.lift()
        self._animate_to(self._open_x())
        self.master.bind("<Button-1>", self._on_outside_click, add="+")

    def close(self) -> None:
        """Close the drawer with a sliding animation."""

        self._is_open = False
        self._animate_to(self._closed_x())
        try:
            self.master.unbind("<Button-1>")
        except Exception:
            pass

    def toggle(self) -> None:
        """Toggle drawer visibility."""

        if self._is_open:
            self.close()
        else:
            self.open()

    def _activate_item(self, target: IHMenuItem, command) -> None:
        for item in self._items:
            item.set_active(item is target)
        if command:
            command()

    def _place_initial(self) -> None:
        self.place(x=self._closed_x(), y=0, width=self.drawer_width, relheight=1)

    def _open_x(self) -> int:
        if self.side == "left":
            return 0
        return max(self.master.winfo_width() - self.drawer_width, 0)

    def _closed_x(self) -> int:
        if self.side == "left":
            return -self.drawer_width
        return max(self.master.winfo_width(), 0)

    def _animate_to(self, target_x: int) -> None:
        if self._animation_job is not None:
            self.after_cancel(self._animation_job)
            self._animation_job = None
        self._step_animation(target_x)

    def _step_animation(self, target_x: int) -> None:
        current_x = self.winfo_x()
        if current_x == target_x:
            self._animating = False
            return
        self._animating = True
        direction = 1 if target_x > current_x else -1
        next_x = current_x + direction * self.animation_step
        if (direction > 0 and next_x > target_x) or (direction < 0 and next_x < target_x):
            next_x = target_x
        self.place_configure(x=next_x)
        self._animation_job = self.after(self.animation_delay, lambda: self._step_animation(target_x))

    def _on_outside_click(self, event) -> None:
        """Cerrá el drawer si el click fue fuera de su área."""
        if not self._is_open:
            return
        dx = self.winfo_rootx()
        dy = self.winfo_rooty()
        dw = self.winfo_width()
        dh = self.winfo_height()
        if not (dx <= event.x_root < dx + dw and dy <= event.y_root < dy + dh):
            self.close()

    def _on_parent_configure(self, _event=None) -> None:
        if self._animating:
            return
        self.place_configure(x=self._open_x() if self._is_open else self._closed_x())
