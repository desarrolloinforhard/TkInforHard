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
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=14)
        self.content = ttk.Frame(self.canvas, style="IH.TFrame")
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.content.bind("<Configure>", self._update_region)
        self.canvas.bind("<Configure>", self._update_width)
        # Bind enter/leave on the canvas (topmost widget inside the frame)
        self.canvas.bind("<Enter>", self._activate_scroll)
        self.canvas.bind("<Leave>", self._deactivate_scroll)

    def _activate_scroll(self, _event=None) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _deactivate_scroll(self, _event=None) -> None:
        # Only deactivate if the cursor truly left the scroll frame area,
        # not just moved into a child widget (card, label, etc.)
        try:
            x, y = self.winfo_rootx(), self.winfo_rooty()
            w, h = self.winfo_width(), self.winfo_height()
            px, py = self.winfo_pointerx(), self.winfo_pointery()
            if not (x <= px <= x + w and y <= py <= y + h):
                self.canvas.unbind_all("<MouseWheel>")
        except Exception:
            self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event) -> None:
        self.canvas.yview_scroll(int(-3 * (event.delta / 120)), "units")

    def _update_region(self, _event=None) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _update_width(self, event) -> None:
        self.canvas.itemconfigure(self.window_id, width=event.width)
