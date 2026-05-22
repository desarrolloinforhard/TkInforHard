"""Deferred frame renderer with a loading state."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHRenderHost(ttk.Frame):
    """Host that renders frames behind a loader before swapping them in."""

    def __init__(self, master=None, loading_text: str = "Cargando...", render_delay: int = 50, **kwargs):
        super().__init__(master, style="IH.TFrame", **kwargs)
        self.loading_text = loading_text
        self.render_delay = render_delay
        self.current = None
        self._loading = None
        self._progress = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def show(self, factory: Callable[["IHRenderHost"], Any], on_ready: Callable[[Any], None] | None = None) -> None:
        """Show a loader, build the next frame, then swap it into view."""

        self._show_loading()
        self.after(self.render_delay, lambda: self._render(factory, on_ready))

    def _show_loading(self) -> None:
        if self._loading is not None:
            self._loading.destroy()

        self._loading = ttk.Frame(self, padding=24, style="IH.Surface.TFrame")
        self._loading.columnconfigure(0, weight=1)
        self._loading.rowconfigure(0, weight=1)

        box = ttk.Frame(self._loading, padding=18, style="IH.Surface.TFrame")
        box.grid(row=0, column=0)
        ttk.Label(box, text=self.loading_text, style="IH.TLabel").pack(anchor="center")
        self._progress = ttk.Progressbar(box, mode="indeterminate", bootstyle="success-striped", length=240)
        self._progress.pack(fill="x", pady=(10, 0))
        self._progress.start(10)

        self._loading.grid(row=0, column=0, sticky="nsew")
        self._loading.lift()
        self.update_idletasks()

    def _render(self, factory: Callable[["IHRenderHost"], Any], on_ready: Callable[[Any], None] | None) -> None:
        next_frame = factory(self)
        try:
            next_frame.grid(row=0, column=0, sticky="nsew")
            next_frame.lower()
            self.update_idletasks()
        except Exception:
            pass

        previous = self.current
        self.current = next_frame

        if previous is not None:
            previous.destroy()

        try:
            next_frame.lift()
        except Exception:
            pass

        self._hide_loading()
        if on_ready is not None:
            on_ready(next_frame)

    def _hide_loading(self) -> None:
        if self._progress is not None:
            self._progress.stop()
            self._progress = None
        if self._loading is not None:
            self._loading.destroy()
            self._loading = None
