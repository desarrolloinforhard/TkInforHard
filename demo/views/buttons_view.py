"""Button showcase view."""

from TkInforHard.layout import IHPage, IHStack
from TkInforHard.widgets import IHButton, IHIconButton, IHSectionHeader, IHToggleButton


class ButtonsView(IHPage):
    """Shows button components."""

    def __init__(self, master=None):
        super().__init__(master)
        IHSectionHeader(self, title="Buttons", subtitle="Acciones semanticas y estados reutilizables.").pack(fill="x")
        stack = IHStack(self)
        stack.pack(fill="x", pady=16)
        for variant in ("primary", "success", "info", "warning", "danger", "secondary"):
            stack.add(IHButton(stack, text=f"Boton {variant}", variant=variant))
        stack.add(IHButton(stack, text="Outline success", variant="success", outline=True))
        stack.add(IHIconButton(stack, icon="⚙", text="Configurar", variant="secondary", outline=True))
        stack.add(IHToggleButton(stack, text="Toggle activo", variant="success"))

