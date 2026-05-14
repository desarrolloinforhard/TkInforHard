"""Inputs showcase view."""

from TkInforHard.layout import IHPage, IHStack
from TkInforHard.widgets import IHCombobox, IHDateInput, IHInput, IHSearchInput, IHSectionHeader, IHTextArea


class InputsView(IHPage):
    """Shows form input components."""

    def __init__(self, master=None):
        super().__init__(master)
        IHSectionHeader(self, title="Inputs", subtitle="Formularios limpios para herramientas internas.").pack(fill="x")
        stack = IHStack(self)
        stack.pack(fill="x", pady=16)
        stack.add(IHInput(stack, label="Cliente", helper="Nombre fiscal o fantasia"))
        stack.add(IHSearchInput(stack, label="Buscar producto"))
        stack.add(IHCombobox(stack, label="Sucursal", values=("Central", "Deposito", "Showroom")))
        stack.add(IHDateInput(stack))
        stack.add(IHTextArea(stack, label="Observaciones", height=4), fill="both")

