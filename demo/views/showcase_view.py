"""Main showcase view."""

from TkInforHard.layout import IHGrid, IHPage, IHScrollFrame
from TkInforHard.widgets import IHBadge, IHDrawerMenu, IHInfoCard, IHMetricCard, IHSectionHeader


class ShowcaseView(IHPage):
    """Overview of the design system and component library."""

    def __init__(self, master=None):
        super().__init__(master)
        scroll = IHScrollFrame(self)
        scroll.pack(fill="both", expand=True)
        IHSectionHeader(
            scroll.content,
            title="TkInforHard UI Framework",
            subtitle="Componentes reutilizables para ERP, POS, verificadores, totens y herramientas internas.",
        ).pack(fill="x", pady=(0, 18))

        grid = IHGrid(scroll.content, columns=3)
        grid.pack(fill="x")
        cards = [
            IHMetricCard(grid, title="Componentes", value="29", delta="Arquitectura escalable"),
            IHMetricCard(grid, title="Themes", value="Light / Dark", delta="Centralizados"),
            IHMetricCard(grid, title="Tokens", value="100%", delta="Sin colores hardcodeados en la API"),
        ]
        for index, card in enumerate(cards):
            grid.add(card, index)

        IHInfoCard(
            scroll.content,
            title="Filosofia",
            body="La demo consume TkInforHard como framework. Los proyectos futuros usan IHButton, IHCard e IHTable en lugar de ttk directo.",
        ).pack(fill="x", pady=(18, 0))
        IHBadge(scroll.content, text="v1.1.0 async loading").pack(anchor="w", pady=(12, 0))

        drawer = IHDrawerMenu(self, title="Panel rapido", side="right", width=260)
        drawer.add_item("Cambios")
        drawer.add_item("Local")
        drawer.add_item("Confirmacion")
        drawer.create_toggle_button(scroll.content, text="Abrir panel", variant="success", outline=True).pack(anchor="w", pady=(14, 0))
