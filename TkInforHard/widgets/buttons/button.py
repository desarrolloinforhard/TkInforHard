"""Button component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHButton(ttk.Button):
    """Semantic action button with TkInforHard variants and sizing."""

    def __init__(
        self,
        master=None,
        text: str = "",
        variant: str = "primary",
        outline: bool = False,
        rounded: bool = True,
        size: str = "md",
        **kwargs,
    ):
        bootstyle = f"outline-{variant}" if outline else variant
        style = f"IH.outline-{variant}.TButton" if outline else f"IH.{variant}.TButton"
        kwargs.setdefault("bootstyle", bootstyle)
        kwargs.setdefault("style", style)
        super().__init__(master, text=text, **kwargs)
        self.variant = variant
        self.outline = outline
        self.rounded = rounded
        self.size = size

