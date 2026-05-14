"""Date input component."""

from TkInforHard.widgets.inputs.input import IHInput


class IHDateInput(IHInput):
    """Date entry using an ISO-friendly text representation."""

    def __init__(self, master=None, label: str | None = "Fecha", placeholder: str = "YYYY-MM-DD", **kwargs):
        super().__init__(master, label=label, **kwargs)
        self.placeholder = placeholder
        self.entry.insert(0, placeholder)

