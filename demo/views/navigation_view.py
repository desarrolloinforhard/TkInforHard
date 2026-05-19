"""Navigation showcase view."""

from TkInforHard.layout import IHPage, IHStack
from TkInforHard.widgets import IHBreadcrumb, IHMenuItem, IHSectionHeader


class NavigationView(IHPage):
    """Shows reusable navigation components."""

    def __init__(self, master=None):
        super().__init__(master)
        IHSectionHeader(self, title="Navigation", subtitle="Sidebar items, breadcrumbs y paneles deslizables.").pack(fill="x")
        stack = IHStack(self)
        stack.pack(fill="x", pady=16)
        stack.add(IHBreadcrumb(stack, items=("Inicio", "Configuracion", "Usuarios")))
        stack.add(IHMenuItem(stack, text="Item activo", active=True, width=220))
        stack.add(IHMenuItem(stack, text="Item normal", width=220))
