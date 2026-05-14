"""Tables showcase view."""

from TkInforHard.layout import IHPage
from TkInforHard.widgets import IHEmptyState, IHFilterBar, IHPagination, IHSectionHeader, IHTable


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
        IHEmptyState(self, title="Sin resultados", message="Estado reutilizable para busquedas vacias.").pack(fill="x")

