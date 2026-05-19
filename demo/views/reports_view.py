"""Reports showcase view."""

from TkInforHard.layout import IHPage
from TkInforHard.widgets import (
    IHStatusCard, IHSectionHeader, IHFilterBar, IHProgress
)
from TkInforHard.widgets.data.rounded_tableview import RoundedTableview
from TkInforHard.theme.tokens import get_tokens
from TkInforHard.utils.canvas import draw_rounded_rect
import tkinter as tk


class ReportsView(IHPage):
    """Showcase de componentes de reporting: status cards + tabla + filtros."""

    SEMAFORO_LIGHT = {
        "verde":    ("#c8e6c9", "#1a202c", "#4a5568"),
        "amarillo": ("#ffecb3", "#1a202c", "#4a5568"),
        "rojo":     ("#ffcdd2", "#1a202c", "#4a5568"),
    }
    SEMAFORO_DARK = {
        "verde":    ("#0D3320", "#22C55E", "#FFFFFF"),
        "amarillo": ("#3D2B00", "#FBBF24", "#FFFFFF"),
        "rojo":     ("#3A1D23", "#F87171", "#FFFFFF"),
    }
    COLUMNAS = [
        {"text": "Fecha",        "stretch": False, "width": 155},
        {"text": "ID",           "stretch": False, "width": 120},
        {"text": "Referencia",   "stretch": False, "width": 145},
        {"text": "Monto",        "stretch": False, "width": 100, "anchor": "e"},
        {"text": "Estado",       "stretch": False, "width": 100},
        {"text": "Caja",         "stretch": True,  "width": 140},
    ]
    SAMPLE_ROWS = [
        ("2026-05-18 10:23:01", "155157698405", "X-0024-00000762",
         "$11,549.89", "approved",  "Caja 01 - Centro",   "verde"),
        ("2026-05-18 10:22:45", "155914334462", "X-0024-00000761",
         "$100.00",    "refunded",  "Caja 02 - Norte",    "amarillo"),
        ("2026-05-18 09:15:10", "125908230694", "X-0024-00000727",
         "$21,598.75", "rejected",  "RECUPERACION SW",    "rojo"),
        ("2026-05-18 09:10:32", "125357800463", "X-0024-00000726",
         "$21,598.75", "approved",  "Caja 01 - Centro",   "verde"),
        ("2026-05-18 08:41:30", "124833302563", "X-0024-00000719",
         "$65.00",     "approved",  "RECUPERACION SW",    "verde"),
    ]

    def __init__(self, master=None):
        super().__init__(master)
        self._build()

    def _build(self):
        IHSectionHeader(
            self,
            title="Reporte de Ventas",
            subtitle="Demo de IHStatusCard + RoundedTableview + IHFilterBar"
        ).pack(fill="x", pady=(0, 12))

        # ── Filtros ────────────────────────────────────────────────────────
        self.filterbar = IHFilterBar(self, fields=[
            {"type": "date",   "key": "desde",   "label": "Desde"},
            {"type": "date",   "key": "hasta",   "label": "Hasta"},
            {"type": "combo",  "key": "estado",  "label": "Estado",
             "values": ["(Todos)", "approved", "refunded", "rejected"]},
            {"type": "button", "key": "generar", "label": "Generar",
             "variant": "primary", "command": self._simular_carga},
        ])
        self.filterbar.pack(fill="x", pady=(0, 8))

        # ── Progress loader ────────────────────────────────────────────────
        self.loader = IHProgress(self, mode="indeterminate")
        # No hace pack todavía — aparece solo al cargar

        # ── Status cards ───────────────────────────────────────────────────
        cards_frame = tk.Frame(self, bg=self._get_bg())
        cards_frame.pack(fill="x", pady=(0, 8))

        pal = self._palette()
        self.card_verde = IHStatusCard(
            cards_frame,
            title="Aprobados con monto coincidente",
            count="0", detail="transacciones · $0.00",
            bg=pal["verde"][0], fg=pal["verde"][1], muted=pal["verde"][2],
        )
        self.card_verde.grid(row=0, column=0, padx=6, sticky="nsew")

        self.card_amarillo = IHStatusCard(
            cards_frame,
            title="Montos distintos o pendientes",
            count="0", detail="transacciones · $0.00",
            bg=pal["amarillo"][0], fg=pal["amarillo"][1], muted=pal["amarillo"][2],
        )
        self.card_amarillo.grid(row=0, column=1, padx=6, sticky="nsew")

        self.card_rojo = IHStatusCard(
            cards_frame,
            title="Sin registro o cancelados",
            count="0", detail="transacciones · $0.00",
            bg=pal["rojo"][0], fg=pal["rojo"][1], muted=pal["rojo"][2],
        )
        self.card_rojo.grid(row=0, column=2, padx=6, sticky="nsew")

        for col in range(3):
            cards_frame.columnconfigure(col, weight=1)

        # ── Tabla ──────────────────────────────────────────────────────────
        tokens = get_tokens(self._theme_name())
        header_fill = tokens["color"]["primary"]

        self.table = RoundedTableview(
            self,
            coldata=self.COLUMNAS,
            rowdata=[],
            bootstyle="primary",
            searchable=False,
            paginated=True,
            pagesize=20,
            autofit=False,
            stripecolor=None,
            pagination_fill=header_fill,
            pagination_outer_bg=self._get_bg(),
            pagination_text_fg="#FFFFFF",
            pagination_radius=10,
        )
        self._build_column_header()
        self.table.pack(fill="both", expand=True)
        self.table.view.configure(show="")

        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")

    def _build_column_header(self):
        tokens = get_tokens(self._theme_name())
        fill = tokens["color"]["primary"]

        self._col_header_canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=fill, height=32)
        self._col_header_frame = tk.Frame(self._col_header_canvas, bg=fill)
        win = self._col_header_canvas.create_window(0, 0, anchor="nw", window=self._col_header_frame)

        for col in self.COLUMNAS:
            anchor = col.get("anchor", "w")
            lbl = tk.Label(
                self._col_header_frame,
                text=col["text"],
                bg=fill,
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                width=col["width"] // 7,
                anchor=anchor,
            )
            lbl.pack(side="left", padx=2, pady=4)

        def _on_resize(event):
            cw, ch = event.width, event.height
            if cw < 10 or ch < 10:
                return
            self._col_header_canvas.itemconfig(win, width=cw, height=ch)
            self._col_header_canvas.delete("ch_rr")
            draw_rounded_rect(self._col_header_canvas, 0, 0, cw, ch, 10, fill, "ch_rr")
            self._col_header_canvas.tag_lower("ch_rr")

        self._col_header_canvas.bind("<Configure>", _on_resize)
        self._col_header_canvas.pack(fill="x", pady=(0, 2))

    def _simular_carga(self):
        """Simula una carga de 2 segundos y carga datos de ejemplo."""
        self.filterbar.set_state("generar", "disabled")
        self.loader.pack(fill="x", pady=(0, 6))
        self.loader.start()
        self.after(2000, self._cargar_datos)

    def _cargar_datos(self):
        self.loader.stop()
        self.loader.pack_forget()
        self.filterbar.set_state("generar", "normal")

        self.table.delete_rows()
        semaforos = []
        for row in self.SAMPLE_ROWS:
            semaforo = row[-1]
            valores = list(row[:-1])
            r = self.table.insert_row("end", valores, reload=False)
            semaforos.append((r, semaforo))

        tag_colors = self._tag_colors()
        for tag, (bg, fg) in tag_colors.items():
            self.table.view.tag_configure(tag, background=bg, foreground=fg)

        for r, semaforo in semaforos:
            r.build()
            self.table.view.item(r.iid, tags=[semaforo])
            self.table.view.detach(r.iid)

        self.table.goto_first_page()

        verde    = sum(1 for r in self.SAMPLE_ROWS if r[-1] == "verde")
        amarillo = sum(1 for r in self.SAMPLE_ROWS if r[-1] == "amarillo")
        rojo     = sum(1 for r in self.SAMPLE_ROWS if r[-1] == "rojo")
        self.card_verde.update(str(verde),       "transacciones · $0.00")
        self.card_amarillo.update(str(amarillo), "transacciones · $0.00")
        self.card_rojo.update(str(rojo),         "transacciones · $0.00")

    def _on_theme_changed(self, _event=None):
        pal = self._palette()
        self.card_verde.set_colors(*pal["verde"])
        self.card_amarillo.set_colors(*pal["amarillo"])
        self.card_rojo.set_colors(*pal["rojo"])
        tokens = get_tokens(self._theme_name())
        header_fill = tokens["color"]["primary"]
        bg = self._get_bg()
        self.table.apply_theme(fill=header_fill, outer_bg=bg, fg="#FFFFFF")
        cur_fill = header_fill
        if self._col_header_canvas:
            w = self._col_header_canvas.winfo_width()
            h = self._col_header_canvas.winfo_height()
            self._col_header_canvas.delete("ch_rr")
            draw_rounded_rect(self._col_header_canvas, 0, 0, w, h, 10, cur_fill, "ch_rr")
            self._col_header_canvas.tag_lower("ch_rr")
            self._col_header_canvas.configure(bg=cur_fill)
            self._col_header_frame.configure(bg=cur_fill)
            for w_ in self._col_header_frame.winfo_children():
                w_.configure(bg=cur_fill)

    def _theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _palette(self) -> dict:
        is_dark = "dark" in self._theme_name()
        return self.SEMAFORO_DARK if is_dark else self.SEMAFORO_LIGHT

    def _tag_colors(self) -> dict:
        is_dark = "dark" in self._theme_name()
        if is_dark:
            return {
                "verde":    ("#0D3320", "#FFFFFF"),
                "amarillo": ("#3D2B00", "#FFFFFF"),
                "rojo":     ("#3A1D23", "#FFFFFF"),
            }
        return {
            "verde":    ("#d4edda", "#155724"),
            "amarillo": ("#fff3cd", "#856404"),
            "rojo":     ("#f8d7da", "#721c24"),
        }

    def _get_bg(self) -> str:
        try:
            tokens = get_tokens(self._theme_name())
            return tokens["color"]["background"]
        except Exception:
            return "#15191D"
