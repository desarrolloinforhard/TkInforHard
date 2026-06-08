"""Canvas-backed rounded button component."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.theme.tokens import get_tokens


SIZE_TOKENS = {
    "sm": {"height": 30, "pad_x": 10, "font_size": 10, "min_width": 82},
    "md": {"height": 34, "pad_x": 11, "font_size": 10, "min_width": 96},
    "lg": {"height": 40, "pad_x": 14, "font_size": 11, "min_width": 112},
}


class IHButton(ttk.Frame):
    """Semantic canvas button with real rounded corners.

    The component keeps the public API close to a regular button while drawing
    its own shape through Canvas so radius is consistent across ttk themes.
    """

    def __init__(
        self,
        master=None,
        text: str = "",
        variant: str = "primary",
        outline: bool = False,
        rounded: bool = True,
        size: str = "md",
        command=None,
        min_width: int | None = None,
        radius: int | None = None,
        state: str = "normal",
        **kwargs,
    ):
        self.text = text
        self.variant = variant
        self.outline = outline
        self.rounded = rounded
        self.size = size if size in SIZE_TOKENS else "md"
        self.command = command
        self.button_state = state
        self.hovered = False
        self.pressed = False
        self.radius_override = radius
        self._size = SIZE_TOKENS[self.size]
        self._tokens = self._resolve_tokens()
        self._font = (self._tokens["font"]["family"], self._size["font_size"], "bold")
        width = kwargs.pop("width", None)
        cursor = kwargs.pop("cursor", "hand2")
        takefocus = kwargs.pop("takefocus", True)
        self.min_width = min_width or self._resolve_width(width)
        super().__init__(master, width=self.min_width, height=self._size["height"], style="IH.Surface.TFrame", **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.canvas = tk.Canvas(
            self,
            width=self.min_width,
            height=self._size["height"],
            highlightthickness=0,
            bd=0,
            cursor=cursor,
            takefocus=takefocus,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._draw)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<space>", self._on_keyboard_invoke)
        self.canvas.bind("<Return>", self._on_keyboard_invoke)
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")
        self._draw()

    def configure(self, cnf=None, **kwargs):  # noqa: D401 - mirrors Tk API
        """Configure button options."""

        if "text" in kwargs:
            self.text = kwargs.pop("text")
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        if "state" in kwargs:
            self.button_state = kwargs.pop("state")
        if "variant" in kwargs:
            self.variant = kwargs.pop("variant")
        if "outline" in kwargs:
            self.outline = kwargs.pop("outline")
        result = super().configure(cnf, **kwargs)
        if hasattr(self, "canvas"):
            self._draw()
        return result

    config = configure

    def invoke(self):
        """Invoke the button command when enabled."""

        if self.button_state == "disabled":
            return None
        if self.command:
            return self.command()
        return None

    def set_text(self, text: str) -> None:
        """Update the visible text."""

        self.text = text
        self._draw()

    def _resolve_width(self, width) -> int:
        if isinstance(width, int) and width > 10:
            return width
        text_width = max(len(self.text), 1) * (self._size["font_size"] + 1)
        return max(self._size["min_width"], text_width + self._size["pad_x"] * 2)

    def _resolve_theme_name(self) -> str:
        try:
            top = self.winfo_toplevel()
            return top.theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _variant_color(self) -> str:
        colors = self._tokens["color"]
        return colors.get(self.variant, colors["primary"])

    def _visual_colors(self) -> tuple[str, str, str]:
        colors = self._tokens["color"]
        variant_color = self._variant_color()
        surface = colors["surface"]
        text = colors["text"]
        if self.button_state == "disabled":
            return colors["surface_alt"], colors["border"], colors["muted"]
        if self.outline:
            if self.variant == "topbar_button":
                base = colors.get("topbar", surface)
                hover = colors.get("primary_hover", base)
                fill = hover if self.hovered or self.pressed else base
            else:
                fill = colors["surface_alt"] if self.hovered or self.pressed else surface
            return fill, variant_color, variant_color
        fill = colors["primary_hover"] if self.hovered or self.pressed else variant_color
        return fill, fill, "#ffffff"

    def _radius(self, width: int, height: int) -> int:
        if not self.rounded:
            return 0
        if self.radius_override is not None:
            return self.radius_override
        return min(self._tokens["radius"]["md"], height // 2, width // 2)

    def _draw_rounded_rect(self, x1: int, y1: int, x2: int, y2: int, radius: int, **kwargs) -> None:
        if radius <= 0:
            self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
            return
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        self.canvas.create_polygon(points, smooth=True, splinesteps=24, **kwargs)

    def _draw(self, _event=None) -> None:
        self._tokens = self._resolve_tokens()
        self._font = (self._tokens["font"]["family"], self._size["font_size"], "bold")
        colors = self._tokens["color"]
        width = max(self.canvas.winfo_width(), self.min_width)
        height = max(self.canvas.winfo_height(), self._size["height"])
        fill, border, text_color = self._visual_colors()
        offset = 1 if self.pressed else 0
        self.canvas.delete("all")
        canvas_bg = colors.get("topbar", colors["surface"]) if self.variant == "topbar_button" else colors["surface"]
        self.canvas.configure(background=canvas_bg)
        self._draw_rounded_rect(
            1,
            1 + offset,
            width - 2,
            height - 2 + offset,
            self._radius(width, height),
            fill=fill,
            outline=border,
            width=1,
        )
        self.canvas.create_text(
            width // 2,
            height // 2 + offset,
            text=self.text,
            fill=text_color,
            font=self._font,
        )

    def _on_enter(self, _event=None) -> None:
        self.hovered = True
        self._draw()

    def _on_leave(self, _event=None) -> None:
        self.hovered = False
        self.pressed = False
        self._draw()

    def _on_press(self, _event=None) -> None:
        if self.button_state == "disabled":
            return
        self.canvas.focus_set()
        self.pressed = True
        self._draw()

    def _on_release(self, event=None) -> None:
        if self.button_state == "disabled":
            return
        was_pressed = self.pressed
        self.pressed = False
        self._draw()
        if was_pressed and event is not None:
            inside = 0 <= event.x <= self.canvas.winfo_width() and 0 <= event.y <= self.canvas.winfo_height()
            if inside:
                self.invoke()

    def _on_keyboard_invoke(self, _event=None) -> str:
        self.invoke()
        return "break"

    def _on_theme_changed(self, _event=None) -> None:
        self._draw()

