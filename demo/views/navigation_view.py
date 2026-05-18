"""Navigation showcase view."""

from TkInforHard.layout import IHPage, IHStack
from TkInforHard.widgets import IHBreadcrumb, IHButton, IHDrawerMenu, IHMenuItem, IHSectionHeader


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

        drawer = IHDrawerMenu(self, title="Herramientas", side="right", width=280)
        drawer.add_item("Cambios", active=True)
        drawer.add_item("Local")
        drawer.add_item("Confirmacion")
        drawer.add_widget(IHButton(drawer.content, text="Accion adicional", variant="success", outline=True))
        stack.add(drawer.create_toggle_button(stack, text="Abrir Drawer", variant="success", outline=True))
