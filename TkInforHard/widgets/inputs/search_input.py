"""Search input component."""

from TkInforHard.widgets.inputs.input import IHInput


class IHSearchInput(IHInput):
    """Single-line search field with default search placeholder."""

    def __init__(self, master=None, placeholder: str = "Buscar...", **kwargs):
        super().__init__(master, placeholder=placeholder, **kwargs)
