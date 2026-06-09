"""Kanban board component for generic status-based entities."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.layout import IHScrollFrame
from TkInforHard.widgets.data._collection_helpers import metadata_text
from TkInforHard.widgets.data.empty_state import IHEmptyState
from TkInforHard.widgets.display.badge import IHBadge


class IHKanbanBoard(ttk.Frame):
    """Configurable board for entities that move between statuses."""

    def __init__(
        self,
        master=None,
        columns: list[dict] | None = None,
        cards: list[dict] | None = None,
        on_card_click: Callable[[dict], None] | None = None,
        on_status_change: Callable[[dict, str], None] | None = None,
        **kwargs,
    ):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self.columns = columns or []
        self.cards: list[dict] = []
        self.on_card_click = on_card_click
        self.on_status_change = on_status_change
        self._column_frames: dict[str, ttk.Frame] = {}
        self._column_counts: dict[str, ttk.Label] = {}
        self._build_columns()
        if cards is not None:
            self.load(cards)

    def load(self, cards: list[dict]) -> None:
        """Replace cards and group them by their ``status`` field."""

        self.cards = cards or []
        self._render_cards()

    def _build_columns(self) -> None:
        for child in self.winfo_children():
            child.destroy()
        self._column_frames.clear()
        self._column_counts.clear()
        if not self.columns:
            IHEmptyState(self, title="Sin columnas", message="Configure columnas para mostrar el tablero.").pack(fill="x")
            return
        for index, column in enumerate(self.columns):
            self.columnconfigure(index, weight=1, uniform="kanban")
            wrapper = ttk.Frame(self, style="IH.Card.TFrame", padding=10)
            wrapper.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 6, 0 if index == len(self.columns) - 1 else 6))

            header = ttk.Frame(wrapper, style="IH.Card.TFrame")
            header.pack(fill="x", pady=(0, 8))
            ttk.Label(header, text=str(column.get("title", column.get("status", ""))), style="IH.CardTitle.TLabel").pack(side="left")
            count = IHBadge(header, text="0", variant=str(column.get("variant", "secondary")))
            count.pack(side="right")

            scroll = IHScrollFrame(wrapper)
            scroll.pack(fill="both", expand=True)
            status = str(column.get("status", ""))
            self._column_frames[status] = scroll.content
            self._column_counts[status] = count

    def _render_cards(self) -> None:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for card in self.cards:
            grouped[str(card.get("status", ""))].append(card)

        statuses = [str(column.get("status", "")) for column in self.columns]
        for column in self.columns:
            status = str(column.get("status", ""))
            frame = self._column_frames.get(status)
            if frame is None:
                continue
            for child in frame.winfo_children():
                child.destroy()
            cards = grouped.get(status, [])
            counter = column.get("counter", len(cards))
            self._column_counts[status].configure(text=str(counter))
            if not cards:
                IHEmptyState(frame, title="Sin elementos", message="No hay cards en esta columna.").pack(fill="x")
                continue
            for card in cards:
                self._render_card(frame, card, statuses)

    def _render_card(self, master, card: dict, statuses: list[str]) -> None:
        item = ttk.Frame(master, style="IH.Card.TFrame", padding=(10, 9))
        item.pack(fill="x", pady=(0, 8))

        ttk.Label(item, text=str(card.get("title", "")), style="IH.CardTitle.TLabel", wraplength=260).pack(anchor="w")
        subtitle = card.get("subtitle")
        if subtitle:
            ttk.Label(item, text=str(subtitle), style="IH.CardMuted.TLabel", wraplength=260).pack(anchor="w", pady=(2, 6))

        footer = ttk.Frame(item, style="IH.Card.TFrame")
        footer.pack(fill="x", pady=(6, 0))
        priority = str(card.get("priority", "normal"))
        IHBadge(footer, text=priority, variant=self._priority_variant(priority)).pack(side="left")
        status_var = ttk.StringVar(value=str(card.get("status", "")))
        status_input = ttk.Combobox(footer, textvariable=status_var, values=statuses, state="readonly", width=14, style="IH.TCombobox")
        status_input.pack(side="right")
        status_input.bind("<<ComboboxSelected>>", lambda _event, c=card, v=status_var: self._change_status(c, v.get()))

        meta = metadata_text(card.get("metadata"))
        if meta:
            ttk.Label(item, text=meta, style="IH.CardMuted.TLabel", wraplength=260).pack(anchor="w", pady=(8, 0))
        self._bind_click(item, card)

    def _bind_click(self, widget, card: dict) -> None:
        if isinstance(widget, ttk.Combobox):
            return
        widget.bind("<Button-1>", lambda _event, c=card: self._click_card(c))
        for child in widget.winfo_children():
            self._bind_click(child, card)

    def _click_card(self, card: dict) -> None:
        if self.on_card_click is not None:
            self.on_card_click(card)

    def _change_status(self, card: dict, new_status: str) -> None:
        if self.on_status_change is not None:
            self.on_status_change(card, new_status)

    def _priority_variant(self, priority: str) -> str:
        normalized = priority.lower()
        if normalized in {"high", "alta", "urgent", "urgente"}:
            return "danger"
        if normalized in {"medium", "media"}:
            return "warning"
        if normalized in {"low", "baja"}:
            return "info"
        return "secondary"
