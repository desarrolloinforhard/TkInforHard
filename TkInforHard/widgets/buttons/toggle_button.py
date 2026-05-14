"""Toggle button component."""

import tkinter as tk

from TkInforHard.widgets.buttons.button import IHButton


class IHToggleButton(IHButton):
    """Two-state button backed by a BooleanVar."""

    def __init__(self, master=None, text: str = "", variable: tk.BooleanVar | None = None, command=None, **kwargs):
        self.variable = variable or tk.BooleanVar(value=False)
        self.user_command = command
        super().__init__(master, text=text, command=self._toggle, **kwargs)
        self._sync_text = text

    def _toggle(self) -> None:
        self.variable.set(not self.variable.get())
        if self.user_command:
            self.user_command(self.variable.get())

