"""Timeline component for chronological event streams."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.layout import IHScrollFrame
from TkInforHard.widgets.data._collection_helpers import (
    current_tokens,
    format_datetime,
    metadata_text,
    sort_datetime_value,
    variant_color,
)
from TkInforHard.widgets.data.empty_state import IHEmptyState
from TkInforHard.widgets.feedback.loading import IHLoading


class IHTimeline(ttk.Frame):
    """Reusable chronological timeline for generic events."""

    def __init__(self, master=None, events: list[dict] | None = None, empty_title: str = "Sin eventos", **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self.empty_title = empty_title
        self.events: list[dict] = []
        self._state_widget = None
        self._scroll = IHScrollFrame(self)
        self._scroll.pack(fill="both", expand=True)
        if events is None:
            self._show_empty()
        else:
            self.load(events)

    def load(self, events: list[dict]) -> None:
        """Replace timeline events, ordered chronologically by ``datetime``."""

        self.events = sorted(events or [], key=lambda item: sort_datetime_value(item.get("datetime")))
        self._clear()
        if not self.events:
            self._show_empty()
            return
        for index, event in enumerate(self.events):
            self._render_event(event, index, index == len(self.events) - 1)

    def set_loading(self, loading: bool = True, text: str = "Cargando eventos...") -> None:
        """Toggle the loading state."""

        self._clear()
        if loading:
            loader = IHLoading(self._scroll.content, text=text)
            loader.pack(fill="x")
            loader.start()
            self._state_widget = loader
        else:
            self.load(self.events)

    def _clear(self) -> None:
        for child in self._scroll.content.winfo_children():
            child.destroy()
        self._state_widget = None

    def _show_empty(self) -> None:
        self._clear()
        self._state_widget = IHEmptyState(
            self._scroll.content,
            title=self.empty_title,
            message="No hay eventos para mostrar.",
        )
        self._state_widget.pack(fill="x")

    def _render_event(self, event: dict, index: int, is_last: bool) -> None:
        tokens = current_tokens()
        color = tokens["color"]
        accent = variant_color(tokens, event.get("variant"))

        row = ttk.Frame(self._scroll.content, style="IH.Surface.TFrame")
        row.pack(fill="x", pady=(0, tokens["spacing"]["sm"]))
        marker = tk.Canvas(row, width=34, height=92, highlightthickness=0, bg=color["surface"])
        marker.pack(side="left", fill="y")
        if index > 0:
            marker.create_line(17, 0, 17, 28, fill=color["border"], width=2)
        if not is_last:
            marker.create_line(17, 50, 17, 92, fill=color["border"], width=2)
        marker.create_oval(10, 28, 24, 42, fill=accent, outline=accent)

        body = ttk.Frame(row, style="IH.Card.TFrame", padding=(12, 10))
        body.pack(side="left", fill="x", expand=True)

        header = ttk.Frame(body, style="IH.Card.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text=str(event.get("title", "")), style="IH.CardTitle.TLabel").pack(side="left", anchor="w")
        when = format_datetime(event.get("datetime"))
        if when:
            ttk.Label(header, text=when, style="IH.CardMuted.TLabel").pack(side="right", anchor="e")

        actor = event.get("actor")
        if actor:
            ttk.Label(body, text=str(actor), style="IH.CardMuted.TLabel").pack(anchor="w", pady=(2, 0))
        description = event.get("description")
        if description:
            ttk.Label(body, text=str(description), style="IH.Surface.TLabel", wraplength=760).pack(anchor="w", pady=(6, 0))
        meta = metadata_text(event.get("metadata"))
        if meta:
            ttk.Label(body, text=meta, style="IH.CardMuted.TLabel", wraplength=760).pack(anchor="w", pady=(8, 0))
