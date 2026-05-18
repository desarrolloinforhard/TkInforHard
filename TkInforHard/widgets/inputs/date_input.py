"""Date input component."""

from TkInforHard.widgets.inputs.input import IHInput


class IHDateInput(IHInput):
    """ISO-oriented date field with a reusable visual contract."""

    def __init__(self, master=None, label: str | None = "Fecha", placeholder: str = "YYYY-MM-DD", **kwargs):
        super().__init__(master, label=label, placeholder=placeholder, **kwargs)
