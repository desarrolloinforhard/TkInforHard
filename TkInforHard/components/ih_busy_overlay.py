"""Reusable busy overlay for long-running UI actions."""

from __future__ import annotations

import threading
import time
import tkinter as tk
from collections.abc import Callable
from typing import Any

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.components.ih_loader import IHLoader


class IHBusyOverlay(tk.Frame):
    """Blocking overlay that runs long tasks while keeping Tkinter responsive."""

    def __init__(
        self,
        parent,
        text: str = "Procesando...",
        subtext: str | None = None,
        size: int = 72,
        block_input: bool = True,
        min_visible_ms: int = 700,
        cancellable: bool = False,
        cancel_text: str = "Cancelar",
        mode: str = "dark",
        background: str | None = None,
        primary_color: str = "#008A46",
    ):
        super().__init__(parent, bd=0, highlightthickness=0)
        self.parent = parent
        self.text = text
        self.subtext = subtext
        self.size = size
        self.block_input = block_input
        self.min_visible_ms = max(0, int(min_visible_ms))
        self.cancellable = cancellable
        self.cancel_text = cancel_text
        self.mode = mode
        self.background = background or self._theme_color("background")
        self.primary_color = primary_color
        self._token = 0
        self._started_at = 0.0
        self._cancelled = False
        self._loader: IHLoader | None = None
        self._build()

    def show(self) -> None:
        """Show the overlay above the parent."""

        self._cancelled = False
        self._started_at = time.perf_counter()
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.lift()
        if self.block_input:
            self.grab_set()
        if self._loader is not None:
            self._loader.start()

    def hide(self) -> None:
        """Hide the overlay and stop animation."""

        if self._loader is not None:
            self._loader.stop()
        try:
            if self.grab_current() is self:
                self.grab_release()
        except Exception:
            pass
        self.place_forget()

    def cancel(self) -> None:
        """Mark the active task as cancelled and hide when possible."""

        self._cancelled = True

    def run(
        self,
        task: Callable[[], Any],
        on_success: Callable[[Any], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> None:
        """Run ``task`` in a background thread and resolve callbacks on the UI thread."""

        self._token += 1
        token = self._token
        self.show()

        def worker() -> None:
            try:
                result = task()
            except Exception as exc:  # pragma: no cover - exercised by app code
                self.after(0, lambda: self._finish_error(token, exc, on_error))
                return
            self.after(0, lambda: self._finish_success(token, result, on_success))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_success(
        self,
        token: int,
        result: Any,
        on_success: Callable[[Any], None] | None,
    ) -> None:
        if token != self._token or self._cancelled:
            return
        self._finish(lambda: on_success(result) if on_success is not None else None)

    def _finish_error(
        self,
        token: int,
        exc: Exception,
        on_error: Callable[[Exception], None] | None,
    ) -> None:
        if token != self._token or self._cancelled:
            return
        self._finish(lambda: on_error(exc) if on_error is not None else None)

    def _finish(self, callback: Callable[[], None]) -> None:
        elapsed_ms = int((time.perf_counter() - self._started_at) * 1000)
        delay = max(0, self.min_visible_ms - elapsed_ms)

        def resolve() -> None:
            self.hide()
            callback()

        self.after(delay, resolve)

    def _build(self) -> None:
        self.configure(background=self.background)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        box = tk.Frame(self, bd=0, highlightthickness=0, padx=20, pady=20)
        box.configure(background=self.background)
        box.grid(row=0, column=0)

        self._loader = IHLoader(
            box,
            size=self.size,
            mode=self.mode,
            background=self.background,
            primary_color=self.primary_color,
            text=self.text,
            text_position="bottom",
        )
        self._loader.pack(anchor="center")

        if self.subtext:
            tk.Label(
                box,
                text=self.subtext,
                background=self.background,
                foreground=self._theme_color("muted"),
                font=("Segoe UI", 9),
                bd=0,
                highlightthickness=0,
            ).pack(anchor="center", pady=(8, 0))

        if self.cancellable:
            ttk.Button(box, text=self.cancel_text, command=self.cancel, bootstyle="secondary-outline").pack(
                anchor="center", pady=(14, 0)
            )

    def _theme_color(self, key: str) -> str:
        try:
            return self.winfo_toplevel().theme_manager.tokens()["color"][key]
        except Exception:
            if key == "background":
                return "#F5F7F6" if self.mode == "light" else "#15191D"
            if key == "muted":
                return "#5B6B63" if self.mode == "light" else "#AAB8B0"
            return "#111827" if self.mode == "light" else "#F9FAFB"
