"""Status card component with configurable state color."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.utils.canvas import draw_rounded_rect


class IHStatusCard(ttk.Frame):
    """Card canvas con color de estado configurable.

    Soporta dark/light mode via <<IHThemeChanged>>.

    Parámetros
    ----------
    master       — widget padre
    title        — texto del subtítulo (ej: "Aprobados con monto coincidente")
    count        — valor grande (ej: "80")
    detail       — texto secundario (ej: "transacciones · $240,983.26")
    bg           — color de fondo de la card
    fg           — color del texto principal (número grande)
    muted        — color del texto secundario
    radius       — radio de bordes (default 12)
    icon         — PhotoImage opcional para el subtítulo
    on_theme_change — callable(is_dark) opcional para actualizar colores
                      cuando cambia el tema

    Métodos públicos
    ----------------
    update(count, detail)      Actualiza los labels sin redibujar el canvas.
    set_colors(bg, fg, muted)  Actualiza los colores y redibuja.
    """

    def __init__(
        self,
        master=None,
        title: str = "",
        count: str = "",
        detail: str = "",
        bg: str = "#1C2721",
        fg: str = "#E8F1EC",
        muted: str = "#AAB8B0",
        radius: int = 12,
        icon=None,
        on_theme_change=None,
        **kwargs,
    ):
        self._bg = bg
        self._fg = fg
        self._muted = muted
        self._radius = radius
        self._icon = icon
        self._on_theme_change = on_theme_change
        self._canvas: tk.Canvas | None = None

        super().__init__(master, style="IH.Surface.TFrame", **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=bg)
        self.canvas.pack(fill="both", expand=True)

        self._inner = tk.Frame(self.canvas, bg=bg)
        self._win_id = self.canvas.create_window(0, 0, anchor="nw", window=self._inner)

        self._lbl_count = tk.Label(
            self._inner,
            text=count,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 28, "bold"),
            anchor="w",
        )
        self._lbl_count.pack(anchor="w", padx=16, pady=(14, 2))

        title_frame = tk.Frame(self._inner, bg=bg)
        title_frame.pack(anchor="w", padx=16, pady=(0, 2))
        if icon is not None:
            tk.Label(title_frame, image=icon, bg=bg).pack(side="left", padx=(0, 6))
        self._lbl_title = tk.Label(
            title_frame,
            text=title,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        )
        self._lbl_title.pack(side="left")

        self._lbl_detail = tk.Label(
            self._inner,
            text=detail,
            bg=bg,
            fg=muted,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self._lbl_detail.pack(anchor="w", padx=16, pady=(0, 14))

        self.canvas.bind("<Configure>", self._on_configure)
        self.after(50, lambda: self._redraw(
            self.canvas.winfo_width() or 200,
            self.canvas.winfo_height() or 120,
        ))
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")

    # ── Public ────────────────────────────────────────────────────────────────

    def update(self, count: str, detail: str) -> None:
        """Actualiza los labels sin redibujar el canvas."""

        self._lbl_count.configure(text=count)
        self._lbl_detail.configure(text=detail)

    def set_colors(self, bg: str, fg: str, muted: str) -> None:
        """Actualiza los colores y redibuja."""

        self._bg = bg
        self._fg = fg
        self._muted = muted
        self._apply_colors()
        self._redraw(
            self.canvas.winfo_width(),
            self.canvas.winfo_height(),
        )

    # ── Private ───────────────────────────────────────────────────────────────

    def _apply_colors(self) -> None:
        self._inner.configure(bg=self._bg)
        self._lbl_count.configure(bg=self._bg, fg=self._fg)
        self._lbl_title.configure(bg=self._bg, fg=self._fg)
        self._lbl_detail.configure(bg=self._bg, fg=self._muted)
        for child in self._inner.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=self._bg)
                for sub in child.winfo_children():
                    try:
                        sub.configure(bg=self._bg)
                    except Exception:
                        pass

    def _redraw(self, w: int, h: int) -> None:
        if w < 8 or h < 8:
            return
        self.canvas.configure(bg=self._bg)
        self.canvas.delete("card_rr")
        draw_rounded_rect(self.canvas, 0, 0, w, h, self._radius, self._bg, "card_rr")
        self.canvas.tag_lower("card_rr")
        self.canvas.itemconfigure(self._win_id, width=w, height=h)

    def _on_configure(self, event) -> None:
        self._redraw(event.width, event.height)

    def _on_theme_changed(self, _event=None) -> None:
        if self._on_theme_change is None:
            return
        try:
            theme = self.winfo_toplevel().theme_manager.current_theme
            is_dark = theme == "inforhard_dark"
        except Exception:
            is_dark = True
        self._on_theme_change(is_dark)
