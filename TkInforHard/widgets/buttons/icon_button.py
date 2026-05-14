"""Icon button component."""

from TkInforHard.widgets.buttons.button import IHButton


class IHIconButton(IHButton):
    """Compact button for icon-first actions."""

    def __init__(self, master=None, icon: str = "", text: str = "", tooltip: str | None = None, **kwargs):
        label = text or icon
        if not text:
            kwargs.setdefault("min_width", 42)
        super().__init__(master, text=label, **kwargs)
        self.icon = icon
        self.tooltip = tooltip
