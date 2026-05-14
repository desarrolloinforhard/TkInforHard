"""Menu item component."""

from TkInforHard.widgets.buttons.button import IHButton


class IHMenuItem(IHButton):
    """Sidebar menu item using the button API."""

    def __init__(self, master=None, text: str = "", active: bool = False, **kwargs):
        variant = "success" if active else "secondary"
        kwargs.setdefault("outline", not active)
        super().__init__(master, text=text, variant=variant, **kwargs)
        self.active = active

