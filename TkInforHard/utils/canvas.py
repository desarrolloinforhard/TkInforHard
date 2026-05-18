"""Canvas drawing utilities for TkInforHard."""

import tkinter as tk

__all__ = ["draw_rounded_rect"]


def draw_rounded_rect(
    canvas: tk.Canvas,
    x1: int, y1: int, x2: int, y2: int,
    r: int,
    fill: str,
    tags: str = "",
) -> None:
    """Draw a filled rounded rectangle on a canvas using arcs + rectangles.

    Probado en producción en MP_CONFIGURADOR v1.3.1.
    """
    r = min(r, (x2 - x1) // 2, (y2 - y1) // 2)
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90, fill=fill, outline=fill, tags=tags)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90, fill=fill, outline=fill, tags=tags)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90, fill=fill, outline=fill, tags=tags)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90, fill=fill, outline=fill, tags=tags)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   fill=fill, outline=fill, tags=tags)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, fill=fill, outline=fill, tags=tags)
