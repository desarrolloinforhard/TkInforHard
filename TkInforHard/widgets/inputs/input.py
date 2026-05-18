"""Canvas-backed text input components."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.theme.tokens import get_tokens


class _IHInputSurface(ttk.Frame):
    """Shared canvas surface used by single-line input controls."""

    HEIGHT = 40
    RADIUS = 12

    def __init__(self, master=None, width: int | None = None, state: str = "normal", **kwargs):
        self.surface_state = state
        self.hovered = False
        self.focused = False
        self.error = False
        self._tokens = self._resolve_tokens()
        super().__init__(master, height=self.HEIGHT, style="IH.Surface.TFrame", **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.canvas = tk.Canvas(self, height=self.HEIGHT, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._draw_surface)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")
        if width:
            self.configure(width=width)

    def set_error(self, error: bool = True) -> None:
        """Set the visual error state."""

        self.error = error
        self._draw_surface()

    def set_disabled(self, disabled: bool = True) -> None:
        """Set the visual disabled state."""

        self.surface_state = "disabled" if disabled else "normal"
        self._draw_surface()

    def _resolve_theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _surface_colors(self) -> tuple[str, str]:
        token = self._tokens["input"]
        if self.surface_state == "disabled":
            return token["disabled"], token["border"]
        if self.error:
            return token["background"], token["error"]
        if self.focused:
            return token["background"], token["border_focus"]
        if self.hovered:
            return token["background_hover"], token["border_hover"]
        return token["background"], token["border"]

    def _draw_rounded_rect(self, width: int, height: int, fill: str, outline: str) -> None:
        x1, y1, x2, y2 = 1, 1, width - 2, height - 2
        radius = min(self.RADIUS, height // 2)
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
        self.canvas.create_polygon(points, smooth=True, splinesteps=24, fill=fill, outline=outline, width=1)

    def _draw_surface(self, _event=None) -> None:
        self._tokens = self._resolve_tokens()
        colors = self._tokens["color"]
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), self.HEIGHT)
        fill, outline = self._surface_colors()
        self.canvas.delete("surface")
        self.canvas.configure(background=colors["surface"])
        self._draw_rounded_rect(width, height, fill, outline)
        self.canvas.tag_lower("all")

    def _on_enter(self, _event=None) -> None:
        self.hovered = True
        self._draw_surface()

    def _on_leave(self, _event=None) -> None:
        self.hovered = False
        self._draw_surface()

    def _on_theme_changed(self, _event=None) -> None:
        self._draw_surface()


class IHInput(ttk.Frame):
    """Labeled single-line input with canvas-rounded field chrome."""

    def __init__(
        self,
        master=None,
        label: str | None = None,
        helper: str | None = None,
        placeholder: str | None = None,
        variable=None,
        state: str = "normal",
        **kwargs,
    ):
        super().__init__(master, style="IH.Surface.TFrame")
        self.variable = variable or tk.StringVar()
        self.placeholder = placeholder
        self.helper_text = helper
        self._placeholder_active = False
        self._tokens = self._resolve_tokens()
        if label:
            ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(anchor="w", pady=(0, 5))
        self.surface = _IHInputSurface(self, state=state)
        self.surface.pack(fill="x")
        self.entry = tk.Entry(
            self.surface,
            textvariable=self.variable,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=(self._tokens["font"]["family"], 10),
        )
        self.entry_window = self.surface.canvas.create_window(12, 20, anchor="w", window=self.entry)
        self.surface.canvas.bind("<Configure>", self._resize_entry, add="+")
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyRelease>", self._sync_placeholder)
        self.helper_label = None
        if helper:
            self.helper_label = ttk.Label(self, text=helper, style="IH.CardMuted.TLabel")
            self.helper_label.pack(anchor="w", pady=(5, 0))
        self._apply_entry_colors()
        self._show_placeholder_if_needed()

    def get(self) -> str:
        """Return the current input value."""

        return "" if self._placeholder_active else self.variable.get()

    def set(self, value: str) -> None:
        """Replace the current input value."""

        self._placeholder_active = False
        self.variable.set(value)
        self._apply_entry_colors()

    def set_error(self, message: str | None = None) -> None:
        """Enable error state and optionally replace helper text."""

        self.surface.set_error(True)
        if message and self.helper_label is not None:
            self.helper_label.configure(text=message)

    def clear_error(self) -> None:
        """Disable error state."""

        self.surface.set_error(False)

    def _resolve_theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _resize_entry(self, event) -> None:
        self.surface.canvas.itemconfigure(self.entry_window, width=max(event.width - 24, 20))

    def _apply_entry_colors(self) -> None:
        self._tokens = self._resolve_tokens()
        token = self._tokens["input"]
        text_color = token["placeholder"] if self._placeholder_active else self._tokens["color"]["text"]
        self.entry.configure(
            bg=self.surface._surface_colors()[0],
            fg=text_color,
            insertbackground=self._tokens["color"]["text"],
            disabledbackground=token["disabled"],
        )

    def _show_placeholder_if_needed(self) -> None:
        if self.placeholder and not self.variable.get():
            self._placeholder_active = True
            self.variable.set(self.placeholder)
            self._apply_entry_colors()

    def _sync_placeholder(self, _event=None) -> None:
        if self._placeholder_active and self.variable.get() != self.placeholder:
            self._placeholder_active = False
        self._apply_entry_colors()

    def _on_focus_in(self, _event=None) -> None:
        self.surface.focused = True
        if self._placeholder_active:
            self._placeholder_active = False
            self.variable.set("")
        self.surface._draw_surface()
        self._apply_entry_colors()

    def _on_focus_out(self, _event=None) -> None:
        self.surface.focused = False
        self._show_placeholder_if_needed()
        self.surface._draw_surface()
        self._apply_entry_colors()
