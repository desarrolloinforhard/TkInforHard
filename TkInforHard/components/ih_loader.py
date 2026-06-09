"""Corporate circular IH loader."""

from __future__ import annotations

import math
import tkinter as tk

try:
    from PIL import Image, ImageDraw, ImageTk
except Exception:  # pragma: no cover
    Image = ImageDraw = ImageTk = None


class IHLoader(tk.Frame):
    """Canvas-based circular loader with fixed IH initials."""

    LIGHT_MUTED = "#D1D5DB"
    DARK_MUTED = "#374151"

    def __init__(
        self,
        master=None,
        size: int = 48,
        primary_color: str = "#008A46",
        background: str | None = None,
        speed: int = 28,
        ring_width: int | None = None,
        font_family: str = "Segoe UI",
        mode: str = "dark",
        high_quality: bool = True,
        text: str | None = None,
        text_position: str = "none",
        show_percent: bool = False,
        progress_text: str | None = None,
        **kwargs,
    ):
        super().__init__(master, bd=0, highlightthickness=0, **kwargs)
        self.size = self._normalize_size(size)
        self.primary_color = primary_color
        self.background = background
        self.speed = max(8, int(speed))
        self.ring_width = ring_width or self._default_ring_width(self.size)
        self.font_family = font_family
        self.mode = mode
        self.high_quality = high_quality
        self.text = text
        self.text_position = text_position
        self.show_percent = show_percent
        self.progress_text = progress_text
        self.angle = 90
        self.pulse = 0.0
        self._pulse_direction = 1
        self._running = False
        self._after_id = None
        self._image_id = None
        self._photo = None
        self._base_id = None
        self._arc_id = None
        self._text_id = None
        self._label = None

        self.configure(background=self._background_color())
        self.canvas = tk.Canvas(
            self,
            width=self.size,
            height=self.size,
            highlightthickness=0,
            bd=0,
        )
        self._build_layout()
        self.canvas.bind("<Configure>", self._on_configure)
        self._build_items()
        self._draw()

    def start(self) -> None:
        """Start the loader animation."""

        if self._running:
            return
        self._running = True
        self._tick()

    def revolution_ms(self) -> int:
        """Return the approximate time needed for one full visual rotation."""

        return math.ceil(360 / self._angle_step()) * self.speed

    def stop(self) -> None:
        """Stop the loader animation."""

        self._running = False
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self._draw()

    def set_size(self, size: int) -> None:
        """Resize the loader to one of the supported visual sizes."""

        self.size = self._normalize_size(size)
        self.ring_width = self._default_ring_width(self.size)
        self.canvas.configure(width=self.size, height=self.size)
        self._build_items()
        self._draw()

    def set_theme(self, mode: str) -> None:
        """Set visual mode: ``light`` or ``dark``."""

        self.mode = "light" if mode == "light" else "dark"
        self._draw()

    def set_text(self, text: str | None = None, progress_text: str | None = None) -> None:
        """Update the optional label text shown near the loader."""

        self.text = text
        self.progress_text = progress_text
        self._build_layout()
        self._draw()

    def _tick(self) -> None:
        if not self._running:
            return
        self.angle = (self.angle - self._angle_step()) % 360
        self.pulse += 0.08 * self._pulse_direction
        if self.pulse >= 1:
            self.pulse = 1
            self._pulse_direction = -1
        elif self.pulse <= 0:
            self.pulse = 0
            self._pulse_direction = 1
        self._draw()
        self._after_id = self.after(self.speed, self._tick)

    def _draw(self) -> None:
        bg = self._background_color()
        muted = self.LIGHT_MUTED if self.mode == "light" else self.DARK_MUTED
        text_color = self._mix_hex(self.primary_color, "#00A653", 0.25 * self.pulse)

        self.configure(background=bg)
        self.canvas.configure(background=bg)
        if self._label is not None:
            self._label.configure(background=bg, foreground=self._text_foreground(), text=self._label_text())

        if self._uses_image_render():
            self._photo = self._render_ring_image(bg, muted)
            self.canvas.itemconfigure(self._image_id, image=self._photo)
            self.canvas.coords(self._image_id, self.size / 2, self.size / 2)
        else:
            self.canvas.coords(self._base_id, *self._circle_points(0, 360, step=4))
            self.canvas.itemconfigure(self._base_id, fill=muted, width=self.ring_width)
            self.canvas.coords(self._arc_id, *self._circle_points(self.angle, 112, step=3))
            self.canvas.itemconfigure(
                self._arc_id,
                fill=self.primary_color,
                width=self.ring_width,
            )
        self.canvas.coords(self._text_id, self.size / 2, self.size / 2)
        self.canvas.itemconfigure(
            self._text_id,
            text="IH",
            fill=text_color,
            font=(self.font_family, self._font_size(), "bold"),
        )
        self.canvas.tag_raise(self._text_id)

    def _build_layout(self) -> None:
        for child in self.winfo_children():
            child.pack_forget()
        bg = self._background_color()
        self.canvas.configure(width=self.size, height=self.size, background=bg)
        if self._shows_label():
            self._label = tk.Label(
                self,
                text=self._label_text(),
                background=bg,
                foreground=self._text_foreground(),
                font=(self.font_family, 10),
                bd=0,
                highlightthickness=0,
            )
        else:
            self._label = None

        position = self.text_position.lower()
        if self._label is None or position == "none":
            self.canvas.pack()
        elif position == "right":
            self.canvas.pack(side="left")
            self._label.pack(side="left", padx=(10, 0))
        elif position == "top":
            self._label.pack(side="top", pady=(0, 8))
            self.canvas.pack(side="top")
        else:
            self.canvas.pack(side="top")
            self._label.pack(side="top", pady=(8, 0))

    def _build_items(self) -> None:
        """Create Canvas items in z-order: ring, arc, text."""

        self.canvas.delete("all")
        if self._uses_image_render():
            self._photo = self._render_ring_image(self._background_color(), self.LIGHT_MUTED if self.mode == "light" else self.DARK_MUTED)
            self._image_id = self.canvas.create_image(self.size / 2, self.size / 2, image=self._photo)
            self._base_id = self._image_id
            self._arc_id = self._image_id
        else:
            muted = self.LIGHT_MUTED if self.mode == "light" else self.DARK_MUTED
            self._base_id = self.canvas.create_line(
                *self._circle_points(0, 360, step=4),
                fill=muted,
                width=self.ring_width,
                smooth=True,
                splinesteps=36,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
            )
            self._arc_id = self.canvas.create_line(
                *self._circle_points(self.angle, 112, step=3),
                fill=self.primary_color,
                width=self.ring_width,
                smooth=True,
                splinesteps=36,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
            )
        self._text_id = self.canvas.create_text(
            self.size / 2,
            self.size / 2,
            text="IH",
            fill=self.primary_color,
            font=(self.font_family, self._font_size(), "bold"),
        )
        self.canvas.tag_raise(self._text_id)

    def _on_configure(self, event) -> None:
        if event.width <= 1 or event.height <= 1:
            return
        next_size = min(event.width, event.height)
        if abs(next_size - self.size) > 2:
            self.size = self._normalize_size(next_size)
            self.ring_width = self._default_ring_width(self.size)
            self.canvas.configure(width=self.size, height=self.size)
            self._build_items()
            self._draw()

    def _background_color(self) -> str:
        if self.background:
            return self.background
        try:
            return self.master.cget("background")
        except Exception:
            return "#FFFFFF" if self.mode == "light" else "#15191D"

    def _uses_image_render(self) -> bool:
        return self.high_quality and Image is not None and ImageDraw is not None and ImageTk is not None

    def _shows_label(self) -> bool:
        return self.text_position.lower() != "none" and bool(self.text or self.progress_text or self.show_percent)

    def _label_text(self) -> str:
        if self.progress_text:
            return self.progress_text
        return self.text or ""

    def _text_foreground(self) -> str:
        return "#111827" if self.mode == "light" else "#F9FAFB"

    def _render_ring_image(self, background: str, muted: str):
        scale = 4
        size = self.size * scale
        ring_width = self.ring_width * scale
        image = Image.new("RGB", (size, size), background)
        draw = ImageDraw.Draw(image)

        pad = max(4, self.ring_width + 3) * scale
        radius = (size - pad * 2) / 2
        center = size / 2

        base_points = self._scaled_circle_points(center, radius, 0, 360, 2)
        arc_points = self._scaled_circle_points(center, radius, self.angle, 112, 1)
        draw.line(base_points, fill=muted, width=ring_width, joint="curve")
        draw.line(arc_points, fill=self.primary_color, width=ring_width, joint="curve")
        self._draw_round_cap(draw, arc_points[0], ring_width, self.primary_color)
        self._draw_round_cap(draw, arc_points[-1], ring_width, self.primary_color)

        image = image.resize((self.size, self.size), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    @staticmethod
    def _scaled_circle_points(
        center: float,
        radius: float,
        start: float,
        extent: float,
        step: int,
    ) -> list[tuple[float, float]]:
        steps = max(24, math.ceil(abs(extent) / step))
        points = []
        for index in range(steps + 1):
            angle = math.radians(start + (extent * index / steps))
            points.append((center + math.cos(angle) * radius, center - math.sin(angle) * radius))
        return points

    @staticmethod
    def _draw_round_cap(draw, point: tuple[float, float], width: int, color: str) -> None:
        radius = width / 2
        x, y = point
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    def _font_size(self) -> int:
        return max(14, int(self.size * 0.28))

    def _ring_box(self) -> tuple[int, int, int, int]:
        pad = max(4, self.ring_width + 3)
        return (pad, pad, self.size - pad, self.size - pad)

    def _circle_points(self, start: float, extent: float, step: int = 6) -> tuple[float, ...]:
        """Return flattened points for a circular Canvas line."""

        pad = max(4, self.ring_width + 3)
        radius = (self.size - pad * 2) / 2
        center = self.size / 2
        steps = max(8, math.ceil(abs(extent) / step))
        points: list[float] = []
        for index in range(steps + 1):
            angle = math.radians(start + (extent * index / steps))
            points.extend((center + math.cos(angle) * radius, center - math.sin(angle) * radius))
        return tuple(points)

    @staticmethod
    def _normalize_size(size: int) -> int:
        return max(24, min(160, int(size)))

    @staticmethod
    def _default_ring_width(size: int) -> int:
        return max(2, round(size / 16))

    @staticmethod
    def _angle_step() -> int:
        return 8

    @classmethod
    def _mix_hex(cls, start: str, end: str, progress: float) -> str:
        progress = max(0.0, min(1.0, progress))
        s = cls._hex_to_rgb(start)
        e = cls._hex_to_rgb(end)
        mixed = tuple(round(s[index] + (e[index] - s[index]) * progress) for index in range(3))
        return "#{:02x}{:02x}{:02x}".format(*mixed)

    @staticmethod
    def _hex_to_rgb(value: str) -> tuple[int, int, int]:
        normalized = value.strip().lstrip("#")
        if len(normalized) == 3:
            normalized = "".join(char * 2 for char in normalized)
        return tuple(int(normalized[index : index + 2], 16) for index in (0, 2, 4))
