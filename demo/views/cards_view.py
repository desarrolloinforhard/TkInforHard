"""Card showcase view."""

from TkInforHard.layout import IHGrid, IHPage
from TkInforHard.widgets import IHCard, IHInfoCard, IHMetricCard, IHSectionHeader


class CardsView(IHPage):
    """Shows card components."""

    def __init__(self, master=None):
        super().__init__(master)
        IHSectionHeader(self, title="Cards", subtitle="Superficies para dashboards y pantallas empresariales.").pack(fill="x")
        grid = IHGrid(self, columns=3)
        grid.pack(fill="x", pady=16)
        examples = [
            IHMetricCard(grid, title="Ventas", value="$ 1.240.000", delta="+12%"),
            IHMetricCard(grid, title="Tickets", value="842", delta="Hoy"),
            IHInfoCard(grid, title="Operacion", body="Resumen compacto para flujos administrativos."),
            IHCard(grid, title="Card base", subtitle="Contenedor reutilizable"),
        ]
        for index, card in enumerate(examples):
            grid.add(card, index)

