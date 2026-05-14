"""Metric card component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.cards.card import IHCard


class IHMetricCard(IHCard):
    """Card optimized for KPI and dashboard metrics."""

    def __init__(self, master=None, title: str = "", value: str = "", delta: str | None = None, **kwargs):
        super().__init__(master, padding=18, **kwargs)
        ttk.Label(self, text=title, style="IH.CardMuted.TLabel").pack(anchor="w")
        ttk.Label(self, text=value, style="IH.CardTitle.TLabel").pack(anchor="w", pady=(6, 0))
        if delta:
            ttk.Label(self, text=delta, style="IH.CardMuted.TLabel").pack(anchor="w", pady=(4, 0))

