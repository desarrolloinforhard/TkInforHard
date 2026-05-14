"""Container layout primitives."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHContainer(ttk.Frame):
    """Generic surface container."""

    def __init__(self, master=None, padding: int = 16, **kwargs):
        super().__init__(master, padding=padding, style="IH.Surface.TFrame", **kwargs)


class IHStack(IHContainer):
    """Vertical stack helper."""

    def add(self, child, fill: str = "x", pady: int | tuple[int, int] = 6):
        """Pack a child into the stack."""

        child.pack(fill=fill, pady=pady)
        return child

