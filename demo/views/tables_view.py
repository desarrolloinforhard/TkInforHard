"""Tables showcase view."""

import tkinter as tk

from TkInforHard.layout import IHPage
from TkInforHard.widgets import IHEmptyState, IHFilterBar, IHImageGridTable, IHPagination, IHSectionHeader, IHTable


IMAGE_GRID_ITEMS = [
    {"name": "Primary", "color": "#009845"},
    {"name": "Info", "color": "#0ea5e9"},
    {"name": "Success", "color": "#22c55e"},
    {"name": "Warning", "color": "#f59e0b"},
    {"name": "Danger", "color": "#ef4444"},
    {"name": "Slate", "color": "#334155"},
    {"name": "Teal", "color": "#14b8a6"},
    {"name": "Light", "color": "#f8fafc"},
    {"name": "Gray", "color": "#64748b"},
    {"name": "Dark", "color": "#111827"},
]


class TablesView(IHPage):
    """Shows table and data components."""

    def __init__(self, master=None):
        super().__init__(master)
        IHSectionHeader(self, title="Data", subtitle="Tablas, filtros, paginacion y estados vacios.").pack(fill="x")
        IHFilterBar(self).pack(fill="x", pady=(16, 0))
        table = IHTable(
            self,
            columns=("Codigo", "Descripcion", "Precio", "Stock"),
            rows=[
                ("1001", "Monitor 24", "$ 180.000", "12"),
                ("1002", "Teclado mecanico", "$ 85.000", "5"),
                ("1003", "Mouse inalambrico", "$ 42.000", "18"),
            ],
        )
        table.pack(fill="both", expand=True)
        IHPagination(self, page=1, total_pages=8).pack(anchor="e", pady=12)
        IHSectionHeader(
            self,
            title="Image Grid Table",
            subtitle="Grilla paginada para imagenes, iconos o miniaturas con renderer canvas.",
        ).pack(fill="x", pady=(18, 8))
        self.image_grid_status = tk.StringVar(value="Seleccion: Primary")
        IHImageGridTable(
            self,
            items=IMAGE_GRID_ITEMS,
            rows=2,
            columns=5,
            cell_size=48,
            image_factory=self._image_grid_preview,
            image_key_getter=lambda item: item["name"],
            label_getter=lambda item: item["name"],
            on_select=self._select_image_grid_item,
            show_labels=True,
            renderer="canvas",
        ).pack(fill="x")
        tk.Label(self, textvariable=self.image_grid_status, anchor="w").pack(fill="x", pady=(6, 0))
        IHEmptyState(self, title="Sin resultados", message="Estado reutilizable para busquedas vacias.").pack(fill="x")

    def _image_grid_preview(self, item: dict[str, str], size: int | None = None):
        image_size = max(16, int(size or 48))
        image = tk.PhotoImage(width=image_size, height=image_size)
        image.put(item["color"], to=(0, 0, image_size, image_size))
        return image

    def _select_image_grid_item(self, item: dict[str, str]) -> None:
        self.image_grid_status.set(f"Seleccion: {item['name']}")
