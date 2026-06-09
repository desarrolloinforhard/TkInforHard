"""Card showcase view."""

import tkinter as tk

from TkInforHard.layout import IHPage, IHScrollFrame
from TkInforHard.widgets import IHButton, IHCard, IHCardGrid, IHInfoCard, IHMetricCard, IHSectionHeader


class CardsView(IHPage):
    """Shows card components."""

    def __init__(self, master=None):
        super().__init__(master)
        self.selected_label = None
        self.selected_option_var = tk.StringVar(value="Local")
        scroll = IHScrollFrame(self)
        scroll.pack(fill="both", expand=True)
        IHSectionHeader(
            scroll.content,
            title="Cards",
            subtitle="Superficies para dashboards, estados, seleccion y acciones empresariales.",
        ).pack(fill="x")

        metrics = IHCardGrid(scroll.content, columns=3)
        metrics.pack(fill="x", pady=16)
        metric_examples = [
            IHMetricCard(
                metrics,
                title="Ventas",
                value="$ 1.240.000",
                delta="12%",
                delta_variant="success",
                badge="Hoy",
                icon="$",
                variant="elevated",
            ),
            IHMetricCard(
                metrics,
                title="Tickets",
                value="842",
                delta="3% demora",
                delta_variant="warning",
                badge="Soporte",
                icon="#",
                variant="info",
            ),
            IHMetricCard(
                metrics,
                title="Errores",
                value="7",
                delta="2 nuevos",
                delta_variant="danger",
                badge="Critico",
                icon="!",
                variant="danger",
            ),
        ]
        for index, card in enumerate(metric_examples):
            metrics.add(card, index)

        IHSectionHeader(scroll.content, title="Estados", subtitle="Variantes semanticas para lectura rapida.").pack(
            fill="x", pady=(12, 0)
        )
        states = IHCardGrid(scroll.content, columns=4)
        states.pack(fill="x", pady=12)
        for index, variant in enumerate(("success", "info", "warning", "danger")):
            states.add(
                IHInfoCard(
                    states,
                    title=variant.title(),
                    body=f"Card con acento {variant} para estados y alertas operativas.",
                    variant=variant,
                ),
                index,
            )

        IHSectionHeader(scroll.content, title="Seleccion", subtitle="Cards clickeables para elegir opciones.").pack(
            fill="x", pady=(12, 0)
        )
        selectable = IHCardGrid(scroll.content, columns=3)
        selectable.pack(fill="x", pady=12)
        self.option_cards = []
        for index, option in enumerate(("Local", "Delivery", "Retiro")):
            card = IHCard(
                selectable,
                title=option,
                subtitle="Click para seleccionar",
                interactive=True,
                command=lambda value=option: self._select_option(value),
                selected=index == 0,
            )
            self.option_cards.append((option, card))
            selectable.add(card, index)
        selection_card = IHCard(scroll.content, title="Seleccion actual", variant="outlined")
        selection_card.pack(fill="x", pady=(4, 0))
        selection_value = selection_card._label("", role="muted")
        selection_value.configure(textvariable=self.selected_option_var)
        selection_value.pack(anchor="w", pady=(8, 0))
        IHButton(selection_card.content, text="Confirmar", variant="success").pack(anchor="e", pady=(12, 0))

    def _select_option(self, option: str) -> None:
        for name, card in self.option_cards:
            card.set_selected(name == option)
        self.selected_option_var.set(f"{option} seleccionado")
