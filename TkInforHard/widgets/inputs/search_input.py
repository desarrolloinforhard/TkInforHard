"""Search input component."""

from TkInforHard.widgets.inputs.input import IHInput


class IHSearchInput(IHInput):
    """Search entry with a consistent placeholder contract."""

    def __init__(self, master=None, placeholder: str = "Buscar...", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.entry.insert(0, placeholder)

