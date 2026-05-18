import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import X, N
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.localization import MessageCatalog

from TkInforHard.utils.canvas import draw_rounded_rect
from TkInforHard.widgets.buttons.button import IHButton


class RoundedTableview(Tableview):
    """
    Tableview subclass that replaces the plain pagination frame with a
    canvas-backed rounded bar built from IHButton instances.

    Extra constructor kwargs (keyword-only):
        pagination_fill       – background fill of the pagination bar
        pagination_outer_bg   – canvas background (matches card bg); defaults to fill
        pagination_text_fg    – label / button text color
        pagination_radius     – corner radius of the pagination bar

    Call apply_theme(fill, outer_bg, fg) whenever the app theme changes.
    All other Tableview behaviour is unchanged.
    """

    def __init__(
        self,
        master=None,
        *,
        pagination_fill: str = "#dbeafe",
        pagination_outer_bg: str | None = None,
        pagination_text_fg: str = "#1a202c",
        pagination_radius: int = 8,
        **kwargs,
    ):
        # Store styling params before super().__init__ calls _build_tableview_widget,
        # which in turn calls our overridden _build_pagination_frame via Python MRO.
        self._pag_fill = pagination_fill
        self._pag_outer_bg = pagination_outer_bg
        self._pag_text_fg = pagination_text_fg
        self._pag_radius = pagination_radius
        self._pag_canvas: tk.Canvas | None = None
        self._pag_frame: tk.Frame | None = None
        self._pag_win_id = None
        self._pag_buttons: list[IHButton] = []
        self._pag_labels: list[tk.Label] = []
        super().__init__(master, **kwargs)

    # ── Public ────────────────────────────────────────────────────────────────

    def apply_theme(
        self,
        fill: str,
        outer_bg: str | None = None,
        fg: str | None = None,
    ):
        """Update pagination bar colors after a theme change."""
        self._pag_fill = fill
        if outer_bg is not None:
            self._pag_outer_bg = outer_bg
        if fg is not None:
            self._pag_text_fg = fg

        if self._pag_canvas is None:
            return

        cur_out = self._pag_outer_bg if self._pag_outer_bg is not None else fill
        self._pag_canvas.configure(bg=cur_out)

        w = self._pag_canvas.winfo_width()
        h = self._pag_canvas.winfo_height()
        if w > 10 and h > 10:
            self._pag_canvas.delete("pag_rr")
            draw_rounded_rect(self._pag_canvas, 0, 0, w, h, self._pag_radius, fill, "pag_rr")
            self._pag_canvas.tag_lower("pag_rr")

        if self._pag_frame:
            self._pag_frame.configure(bg=fill)

        for lbl in self._pag_labels:
            try:
                lbl.configure(bg=fill, fg=self._pag_text_fg)
            except Exception:
                pass

    # ── Override ──────────────────────────────────────────────────────────────

    def _build_pagination_frame(self):
        fill = self._pag_fill
        out_bg = self._pag_outer_bg if self._pag_outer_bg is not None else fill

        canvas = tk.Canvas(self, bg=out_bg, highlightthickness=0, bd=0, height=38)
        canvas.pack(fill=X, anchor=N, pady=(2, 0))

        frame = tk.Frame(canvas, bg=fill)
        win_id = canvas.create_window(2, 2, window=frame, anchor="nw")

        self._pag_canvas = canvas
        self._pag_frame = frame
        self._pag_win_id = win_id
        self._pag_buttons = []
        self._pag_labels = []

        def _btn(text, cmd):
            b = IHButton(
                frame,
                text=text,
                command=cmd,
                variant="secondary",
                outline=True,
                size="sm",
            )
            self._pag_buttons.append(b)
            return b

        # Right side: reset → last → next → prev → first (pack side=right reads RTL)
        _btn("⎌", self.reset_table).pack(side="right", padx=(0, 6), pady=3)
        _btn("»", self.goto_last_page).pack(side="right", padx=1, pady=3)
        _btn("›", self.goto_next_page).pack(side="right", padx=1, pady=3)
        _btn("‹", self.goto_prev_page).pack(side="right", padx=1, pady=3)
        _btn("«", self.goto_first_page).pack(side="right", padx=(6, 1), pady=3)

        # Page info labels
        lbl_limit = tk.Label(
            frame, textvariable=self._pagelimit,
            bg=fill, fg=self._pag_text_fg, font=("Segoe UI", 9),
        )
        lbl_limit.pack(side="right", padx=(0, 4))
        self._pag_labels.append(lbl_limit)

        lbl_of = tk.Label(
            frame, text=MessageCatalog.translate("of"),
            bg=fill, fg=self._pag_text_fg, font=("Segoe UI", 9),
        )
        lbl_of.pack(side="right", padx=2)
        self._pag_labels.append(lbl_of)

        idx = ttk.Entry(frame, textvariable=self._pageindex, width=4)
        idx.pack(side="right", pady=3)
        idx.bind("<Return>",   self.goto_page, "+")
        idx.bind("<KP_Enter>", self.goto_page, "+")

        lbl_page = tk.Label(
            frame, text=MessageCatalog.translate("Page"),
            bg=fill, fg=self._pag_text_fg, font=("Segoe UI", 9),
        )
        lbl_page.pack(side="right", padx=5)
        self._pag_labels.append(lbl_page)

        # Fit canvas height to content
        frame.update_idletasks()
        canvas.configure(height=frame.winfo_reqheight() + 4)

        def _on_resize(event):
            cw, ch = event.width, event.height
            if cw < 10 or ch < 10:
                return
            canvas.itemconfig(win_id, width=max(cw - 4, 1), height=max(ch - 4, 1))
            canvas.delete("pag_rr")
            draw_rounded_rect(canvas, 0, 0, cw, ch, self._pag_radius, self._pag_fill, "pag_rr")
            canvas.tag_lower("pag_rr")
            frame.configure(bg=self._pag_fill)

        canvas.bind("<Configure>", _on_resize)
