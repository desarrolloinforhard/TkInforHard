"""Canvas-backed card components."""

from __future__ import annotations

import tkinter as tk

from PIL import Image, ImageDraw, ImageTk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.theme.tokens import get_tokens


class IHCard(ttk.Frame):
    """Rounded reusable surface for grouping related content.

    Cards expose an inner ``content`` frame so consumers can compose arbitrary
    children while the outer canvas owns background, border and interaction.
    """

    RADIUS = 12

    def __init__(
        self,
        master=None,
        title: str | None = None,
        subtitle: str | None = None,
        padding: int = 16,
        variant: str = "default",
        interactive: bool = False,
        command=None,
        **kwargs,
    ):
        self.title_text = title
        self.subtitle_text = subtitle
        self.padding = padding
        self.variant = variant
        self.interactive = interactive or command is not None
        self.command = command
        self.hovered = False
        self._tokens = self._resolve_tokens()
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.content = ttk.Frame(self, padding=padding, style="IH.Surface.TFrame")
        self.window_id = self.canvas.create_window(padding, padding, anchor="nw", window=self.content)
        self.canvas.bind("<Configure>", self._draw)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<Button-1>", self._on_click)
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")
        if title:
            ttk.Label(self.content, text=title, style="IH.CardTitle.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(self.content, text=subtitle, style="IH.CardMuted.TLabel").pack(anchor="w", pady=(2, 10))
        self._draw()

    def add(self, child, **pack_options):
        """Pack a child into the card content frame and return it."""

        child.pack(in_=self.content, **pack_options)
        return child

    def _resolve_theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _render_card_image(self, width: int, height: int, background: str, border: str, shadow: str):
        """Render a clean anti-aliased rounded card surface with Pillow."""

        scale = 3
        image = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        radius = self.RADIUS * scale

        if self.variant == "elevated":
            draw.rounded_rectangle(
                (3 * scale, 4 * scale, (width - 2) * scale, (height - 2) * scale),
                radius=radius,
                fill=shadow,
            )

        outline = None if self.variant == "elevated" else border
        draw.rounded_rectangle(
            (1 * scale, 1 * scale, (width - 3) * scale, (height - 3) * scale),
            radius=radius,
            fill=background,
            outline=outline,
            width=scale if outline else 1,
        )
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def _draw(self, _event=None) -> None:
        self._tokens = self._resolve_tokens()
        color = self._tokens["color"]
        card = self._tokens["card"]
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        background = card["background_hover"] if self.hovered and self.interactive else card["background"]
        border = card["border"]
        self.canvas.delete("all")
        self.canvas.configure(background=color["surface"])
        if width < 8 or height < 8:
            return
        self._card_image = self._render_card_image(width, height, background, border, card["shadow"])
        self.canvas.create_image(0, 0, anchor="nw", image=self._card_image)
        self.window_id = self.canvas.create_window(
            self.padding,
            self.padding,
            anchor="nw",
            window=self.content,
            width=max(width - self.padding * 2 - 2, 20),
        )
        self.content.configure(style="IH.Surface.TFrame")

    def _on_enter(self, _event=None) -> None:
        self.hovered = True
        self._draw()

    def _on_leave(self, _event=None) -> None:
        self.hovered = False
        self._draw()

    def _on_click(self, _event=None) -> None:
        if self.command:
            self.command()

    def _on_theme_changed(self, _event=None) -> None:
        self._draw()
