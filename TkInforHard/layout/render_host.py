"""Deferred frame renderer with a loading state."""

from __future__ import annotations

import time
import tkinter as tk
from collections.abc import Callable
from typing import Any

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.components import IHLoader


class IHRenderHost(ttk.Frame):
    """Host that renders frames behind a loader before swapping them in."""

    def __init__(
        self,
        master=None,
        loading_text: str = "Cargando...",
        render_delay: int = 120,
        min_loader_ms: int = 420,
        min_loader_cycles: int = 1,
        settle_delay: int = 80,
        cache_views: bool = True,
        prepare_timeout_ms: int | None = None,
        **kwargs,
    ):
        super().__init__(master, style="IH.TFrame", **kwargs)
        self.loading_text = loading_text
        self.render_delay = render_delay
        self.min_loader_ms = min_loader_ms
        self.min_loader_cycles = max(0, int(min_loader_cycles))
        self.settle_delay = max(0, int(settle_delay))
        self.cache_views = cache_views
        self.prepare_timeout_ms = prepare_timeout_ms
        self.current = None
        self.current_key = None
        self._cache: dict[str, Any] = {}
        self._loading = None
        self._loader = None
        self._loading_started = 0.0
        self._render_token = 0
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def show(
        self,
        factory: Callable[["IHRenderHost"], Any],
        on_ready: Callable[[Any], None] | None = None,
        cache_key: str | None = None,
        on_error: Callable[[Exception], None] | None = None,
        prepare: Callable[[Any, Callable[[], None], Callable[[Exception], None]], None] | None = None,
        timeout_ms: int | None = None,
    ) -> None:
        """Show a loader, build the next frame, then swap it into view."""

        self._render_token += 1
        token = self._render_token
        self._show_loading()
        prepare_delay = max(self.render_delay, self._loader_cycle_ms())
        self.after(
            prepare_delay,
            lambda: self._prepare(token, factory, on_ready, cache_key, on_error, prepare, timeout_ms),
        )

    def _show_loading(self) -> None:
        if self._loading is not None:
            self._loading.destroy()
        self._loading_started = time.perf_counter()

        background = self._surface_background()
        self._loading = tk.Frame(self, bd=0, highlightthickness=0)
        self._loading.configure(background=background)
        self._loading.columnconfigure(0, weight=1)
        self._loading.rowconfigure(0, weight=1)

        box = tk.Frame(self._loading, bd=0, highlightthickness=0, padx=18, pady=18)
        box.configure(background=background)
        box.grid(row=0, column=0)
        label = tk.Label(
            box,
            text=self.loading_text,
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=0,
        )
        label.configure(background=background, foreground=self._text_color())
        label.pack(anchor="center")
        self._loader = IHLoader(box, size=96, mode=self._theme_mode(), background=background, ring_width=5)
        self._loader.pack(anchor="center", pady=(16, 0))
        self._loader.start()

        self._loading.grid(row=0, column=0, sticky="nsew")
        self._loading.lift()
        self.update_idletasks()

    def _prepare(
        self,
        token: int,
        factory: Callable[["IHRenderHost"], Any],
        on_ready: Callable[[Any], None] | None,
        cache_key: str | None,
        on_error: Callable[[Exception], None] | None,
        prepare: Callable[[Any, Callable[[], None], Callable[[Exception], None]], None] | None,
        timeout_ms: int | None,
    ) -> None:
        if token != self._render_token:
            return

        try:
            next_frame = self._resolve_frame(factory, cache_key)
            next_frame.grid(row=0, column=0, sticky="nsew")
            next_frame.lower()
            self.update_idletasks()
        except Exception as exc:
            self._handle_error(token, exc, on_error)
            return

        self._prepare_view(token, next_frame, on_ready, cache_key, on_error, prepare, timeout_ms)

    def _prepare_view(
        self,
        token: int,
        next_frame,
        on_ready: Callable[[Any], None] | None,
        cache_key: str | None,
        on_error: Callable[[Exception], None] | None,
        prepare: Callable[[Any, Callable[[], None], Callable[[Exception], None]], None] | None,
        timeout_ms: int | None,
    ) -> None:
        if not self._should_prepare(next_frame):
            self._finish_prepare(token, next_frame, on_ready, cache_key)
            return

        prepare_callable = prepare or getattr(next_frame, "prepare_for_render", None)
        if prepare_callable is None:
            self._finish_prepare(token, next_frame, on_ready, cache_key)
            return

        done_called = {"value": False}

        def done() -> None:
            if done_called["value"] or token != self._render_token:
                return
            done_called["value"] = True
            try:
                setattr(next_frame, "_ih_prepared_for_render", True)
            except Exception:
                pass
            self._finish_prepare(token, next_frame, on_ready, cache_key)

        def fail(exc: Exception) -> None:
            if done_called["value"] or token != self._render_token:
                return
            done_called["value"] = True
            self._handle_error(token, exc, on_error)

        timeout = timeout_ms if timeout_ms is not None else self.prepare_timeout_ms
        if timeout:
            self.after(timeout, lambda: fail(TimeoutError("La preparacion del modulo tardo demasiado.")))

        try:
            if prepare is not None:
                prepare_callable(next_frame, done, fail)
            else:
                prepare_callable(done, fail)
        except Exception as exc:
            fail(exc)

    def _finish_prepare(
        self,
        token: int,
        next_frame,
        on_ready: Callable[[Any], None] | None,
        cache_key: str | None,
    ) -> None:
        if token != self._render_token:
            return
        elapsed_ms = int((time.perf_counter() - self._loading_started) * 1000)
        required_ms = max(self.min_loader_ms, self._loader_cycle_ms())
        remaining = max(self.settle_delay, required_ms - elapsed_ms)
        self.after(remaining, lambda: self._swap(token, next_frame, on_ready, cache_key))

    def _resolve_frame(self, factory: Callable[["IHRenderHost"], Any], cache_key: str | None):
        if self.cache_views and cache_key and cache_key in self._cache:
            return self._cache[cache_key]

        frame = factory(self)
        if self.cache_views and cache_key:
            self._cache[cache_key] = frame
        return frame

    def _swap(self, token: int, next_frame, on_ready: Callable[[Any], None] | None, cache_key: str | None) -> None:
        if token != self._render_token:
            return

        previous = self.current
        self.current = next_frame
        self.current_key = cache_key

        if previous is not None and previous is not next_frame:
            if self.cache_views:
                previous.grid_remove()
            else:
                previous.destroy()
        elif previous is next_frame:
            next_frame.grid(row=0, column=0, sticky="nsew")

        try:
            next_frame.lift()
        except Exception:
            pass

        self._hide_loading()
        if on_ready is not None:
            on_ready(next_frame)

    def _hide_loading(self) -> None:
        if self._loader is not None:
            self._loader.stop()
            self._loader = None
        if self._loading is not None:
            self._loading.destroy()
            self._loading = None

    def _should_prepare(self, view) -> bool:
        checker = getattr(view, "should_prepare_for_render", None)
        if callable(checker):
            try:
                return bool(checker())
            except Exception:
                return True
        return not bool(getattr(view, "_ih_prepared_for_render", False))

    def _handle_error(
        self,
        token: int,
        exc: Exception,
        on_error: Callable[[Exception], None] | None,
    ) -> None:
        if token != self._render_token:
            return
        self._show_error(exc)
        if on_error is not None:
            on_error(exc)

    def _show_error(self, exc: Exception) -> None:
        self._hide_loading()
        background = self._surface_background()
        panel = tk.Frame(self, bd=0, highlightthickness=0)
        panel.configure(background=background)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=1)
        content = tk.Frame(panel, bd=0, highlightthickness=0, padx=24, pady=24)
        content.configure(background=background)
        content.grid(row=0, column=0)
        tk.Label(
            content,
            text="No se pudo cargar el modulo",
            background=background,
            foreground=self._text_color(),
            font=("Segoe UI", 12, "bold"),
            bd=0,
            highlightthickness=0,
        ).pack(anchor="center")
        tk.Label(
            content,
            text=str(exc),
            background=background,
            foreground=self._muted_color(),
            font=("Segoe UI", 9),
            bd=0,
            highlightthickness=0,
        ).pack(anchor="center", pady=(6, 0))
        panel.grid(row=0, column=0, sticky="nsew")
        panel.lift()
        self._loading = panel

    def _theme_mode(self) -> str:
        try:
            theme = self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            theme = ""
        return "light" if "light" in str(theme).lower() else "dark"

    def _surface_background(self) -> str:
        try:
            tokens = self.winfo_toplevel().theme_manager.tokens()
            return tokens["color"]["background"]
        except Exception:
            return "#F5F7F6" if self._theme_mode() == "light" else "#15191D"

    def _text_color(self) -> str:
        try:
            tokens = self.winfo_toplevel().theme_manager.tokens()
            return tokens["color"]["text"]
        except Exception:
            return "#111827" if self._theme_mode() == "light" else "#F9FAFB"

    def _muted_color(self) -> str:
        try:
            tokens = self.winfo_toplevel().theme_manager.tokens()
            return tokens["color"]["muted"]
        except Exception:
            return "#5B6B63" if self._theme_mode() == "light" else "#AAB8B0"

    def _loader_cycle_ms(self) -> int:
        if self._loader is None or self.min_loader_cycles <= 0:
            return 0
        return self._loader.revolution_ms() * self.min_loader_cycles
