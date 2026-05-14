"""Scrollable frame layout."""

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHScrollFrame(ttk.Frame):
    """Canvas-backed scrollable frame for long forms and showcases."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, style="IH.TFrame", **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = ttk.Frame(self.canvas, style="IH.TFrame")
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.content.bind("<Configure>", self._update_region)
        self.canvas.bind("<Configure>", self._update_width)

    def _update_region(self, _event=None) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _update_width(self, event) -> None:
        self.canvas.itemconfigure(self.window_id, width=event.width)

