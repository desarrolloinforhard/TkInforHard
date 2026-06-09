"""Canvas-backed card components."""

from __future__ import annotations

import tkinter as tk

from PIL import Image, ImageDraw, ImageTk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.theme.tokens import get_tokens
from TkInforHard.utils import IHAnimator


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
        selected: bool = False,
        **kwargs,
    ):
        self.title_text = title
        self.subtitle_text = subtitle
        self.padding = padding
        self.variant = variant
        self.interactive = interactive or command is not None
        self.command = command
        self.selected = selected
        self.hovered = False
        self.pressed = False
        self.hover_progress = 0.0
        self.press_progress = 0.0
        self._tokens = self._resolve_tokens()
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self._hover_animator = IHAnimator(self, duration=140, easing="ease_out")
        self._press_animator = IHAnimator(self, duration=90, easing="ease_out")
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.content = tk.Frame(self.canvas, bd=0, highlightthickness=0)
        self.window_id = self.canvas.create_window(padding, padding, anchor="nw", window=self.content)
        self.canvas.bind("<Configure>", self._draw)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<Button-1>", self._on_click)
        self._bind_card_events(self.content)
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")
        if title:
            self._label(title, role="title").pack(anchor="w")
        if subtitle:
            self._label(subtitle, role="muted").pack(anchor="w", pady=(2, 10))
        self._draw()

    def add(self, child, **pack_options):
        """Pack a child into the card content frame and return it."""

        child.pack(in_=self.content, **pack_options)
        return child

    def set_selected(self, selected: bool = True) -> None:
        """Update the selected state and redraw the card."""

        self.selected = selected
        self._draw()

    def set_variant(self, variant: str) -> None:
        """Update the visual variant and redraw the card."""

        self.variant = variant
        self._draw()

    def _resolve_theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _render_card_image(self, width: int, height: int, background: str, border: str, shadow: str, inset: int):
        """Render a clean anti-aliased rounded card surface with Pillow."""

        scale = 3
        image = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        radius = self.RADIUS * scale
        i = inset * scale

        if self.variant == "elevated":
            draw.rounded_rectangle(
                (max(i, 3 * scale), max(i, 4 * scale), (width - 2 - inset) * scale, (height - 2 - inset) * scale),
                radius=radius,
                fill=shadow,
            )

        outline = None if self.variant == "elevated" and not self.selected else border
        draw.rounded_rectangle(
            ((1 + inset) * scale, (1 + inset) * scale, (width - 3 - inset) * scale, (height - 3 - inset) * scale),
            radius=radius,
            fill=background,
            outline=outline,
            width=(2 * scale) if self.selected else (scale if outline else 1),
        )
        accent = self._variant_color()
        if accent:
            draw.rounded_rectangle(
                ((1 + inset) * scale, (1 + inset) * scale, (6 + inset) * scale, (height - 3 - inset) * scale),
                radius=max(2 * scale, radius // 3),
                fill=accent,
            )
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def _draw(self, _event=None) -> None:
        self._tokens = self._resolve_tokens()
        color = self._tokens["color"]
        card = self._tokens["card"]
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        background = self._mix_hex(card["background"], card["background_hover"], self.hover_progress)
        border = color["primary"] if self.selected else card["border"]
        canvas_background = self._parent_background()
        inset = round(self._lerp(4, 1, self.hover_progress) + self.press_progress * 2)
        self.canvas.delete("all")
        self.canvas.configure(background=canvas_background)
        if width < 8 or height < 8:
            return
        self._card_image = self._render_card_image(width, height, background, border, card["shadow"], inset)
        self.canvas.create_image(0, 0, anchor="nw", image=self._card_image)
        content_padding = self.padding + inset
        self.window_id = self.canvas.create_window(
            content_padding,
            content_padding,
            anchor="nw",
            window=self.content,
            width=max(width - content_padding * 2 - 2, 20),
        )
        self._apply_content_colors(background)

    def _on_enter(self, _event=None) -> None:
        if not self.interactive:
            return
        self.hovered = True
        self._hover_animator.animate_to(1.0, self._set_hover_progress)

    def _on_leave(self, _event=None) -> None:
        if not self.interactive:
            return
        self.hovered = False
        self.pressed = False
        self._press_animator.animate_to(0.0, self._set_press_progress)
        self._hover_animator.animate_to(0.0, self._set_hover_progress)

    def _on_click(self, _event=None) -> None:
        if self.interactive:
            self.pressed = True
            self._press_animator.set(1.0)
            self.press_progress = 1.0
            self._draw()
            self._press_animator.animate_to(0.0, self._set_press_progress, on_done=self._clear_pressed)
        if self.command:
            self.command()

    def _on_theme_changed(self, _event=None) -> None:
        self._draw()

    def _variant_color(self) -> str | None:
        color = self._tokens["color"]
        if self.variant in ("success", "info", "warning", "danger", "primary"):
            return color.get(self.variant, color["primary"])
        if self.selected:
            return color["primary"]
        return None

    def _label(self, text: str, role: str = "muted", parent=None, **kwargs):
        font = self._tokens["font"]
        color = self._tokens["color"]
        label = tk.Label(
            parent or self.content,
            text=text,
            bg=self._tokens["card"]["background"],
            fg=color["text"] if role == "title" else color["muted"],
            font=(font["family"], font["title"], font["bold"]) if role == "title" else (font["family"], font["small"]),
            bd=0,
            highlightthickness=0,
            justify=kwargs.pop("justify", "left"),
            anchor=kwargs.pop("anchor", "w"),
            **kwargs,
        )
        label._ih_card_role = role  # type: ignore[attr-defined]
        self._bind_card_events(label)
        return label

    def _apply_content_colors(self, background: str) -> None:
        self.content.configure(bg=background)
        self._apply_widget_colors(self.content, background)

    def _apply_widget_colors(self, widget, background: str) -> None:
        color = self._tokens["color"]
        for child in widget.winfo_children():
            role = getattr(child, "_ih_card_role", None)
            try:
                child.configure(bg=background)
                if role == "title":
                    child.configure(fg=color["text"])
                elif role == "muted":
                    child.configure(fg=color["muted"])
            except Exception:
                pass
            self._apply_widget_colors(child, background)

    def _bind_card_events(self, widget) -> None:
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        widget.bind("<Button-1>", self._on_click, add="+")

    def _parent_background(self) -> str:
        color = self._tokens["color"]
        try:
            bg = self.master.cget("background")
            if bg:
                return bg
        except Exception:
            pass
        return color["background"]

    def _set_hover_progress(self, value: float) -> None:
        self.hover_progress = value
        self._draw()

    def _set_press_progress(self, value: float) -> None:
        self.press_progress = value
        self._draw()

    def _clear_pressed(self) -> None:
        self.pressed = False

    @staticmethod
    def _lerp(start: float, end: float, progress: float) -> float:
        return start + (end - start) * progress

    @classmethod
    def _mix_hex(cls, start: str, end: str, progress: float) -> str:
        try:
            s = cls._hex_to_rgb(start)
            e = cls._hex_to_rgb(end)
        except Exception:
            return end if progress >= 0.5 else start
        mixed = tuple(round(cls._lerp(s[index], e[index], progress)) for index in range(3))
        return "#{:02x}{:02x}{:02x}".format(*mixed)

    @staticmethod
    def _hex_to_rgb(value: str) -> tuple[int, int, int]:
        normalized = value.strip().lstrip("#")
        if len(normalized) == 3:
            normalized = "".join(char * 2 for char in normalized)
        return tuple(int(normalized[index : index + 2], 16) for index in (0, 2, 4))
