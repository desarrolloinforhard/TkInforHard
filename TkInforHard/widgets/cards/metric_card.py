"""Metric card component."""

import tkinter as tk

from TkInforHard.widgets.cards.card import IHCard


class IHMetricCard(IHCard):
    """Card optimized for KPI and dashboard metrics."""

    def __init__(
        self,
        master=None,
        title: str = "",
        value: str = "",
        delta: str | None = None,
        delta_variant: str = "default",
        badge: str | None = None,
        helper: str | None = None,
        icon: str | None = None,
        variant: str = "default",
        **kwargs,
    ):
        super().__init__(master, padding=18, variant=variant, **kwargs)
        header = tk.Frame(self.content, bd=0, highlightthickness=0)
        header.pack(fill="x")
        self._bind_card_events(header)
        title_text = f"{icon}  {title}" if icon else title
        self._label(title_text, role="muted", parent=header).pack(side="left", anchor="w")
        if badge:
            self._label(badge, role="muted", parent=header).pack(side="right", anchor="e")
        self._label(value, role="title").pack(anchor="w", pady=(7, 0))
        if delta:
            prefix = {"success": "+", "danger": "-", "warning": "!", "info": "i"}.get(delta_variant, "")
            delta_text = f"{prefix} {delta}" if prefix and not delta.startswith(prefix) else delta
            self._label(delta_text, role="muted").pack(anchor="w", pady=(5, 0))
        if helper:
            self._label(helper, role="muted", wraplength=280).pack(
                anchor="w", pady=(5, 0)
            )
