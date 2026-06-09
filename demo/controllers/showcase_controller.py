"""Controller for the demo showcase views."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.layout import IHRenderHost
from demo.views.buttons_view import ButtonsView
from demo.views.cards_view import CardsView
from demo.views.feedback_view import FeedbackView
from demo.views.icons_view import IconsView
from demo.views.inputs_view import InputsView
from demo.views.navigation_view import NavigationView
from demo.views.reports_view import ReportsView
from demo.views.showcase_view import ShowcaseView
from demo.views.tables_view import TablesView


class ShowcaseController:
    """Coordinates view navigation for the demo without defining UI components."""

    def __init__(self, master):
        self.content = IHRenderHost(
            master,
            loading_text="Cargando modulo...",
            render_delay=140,
            min_loader_ms=1300,
            min_loader_cycles=1,
            settle_delay=120,
            cache_views=True,
        )
        self.views = {
            "showcase": ShowcaseView,
            "buttons": ButtonsView,
            "cards": CardsView,
            "inputs": InputsView,
            "icons": IconsView,
            "navigation": NavigationView,
            "tables": TablesView,
            "feedback": FeedbackView,
            "reports": ReportsView,
        }
        self.current = None

    def menu_items(self) -> list[tuple[str, object]]:
        """Return sidebar menu items."""

        return [
            ("Showcase", lambda: self.show("showcase")),
            ("Buttons", lambda: self.show("buttons")),
            ("Cards", lambda: self.show("cards")),
            ("Inputs", lambda: self.show("inputs")),
            ("Iconos", lambda: self.show("icons")),
            ("Navigation", lambda: self.show("navigation")),
            ("Tables", lambda: self.show("tables")),
            ("Feedback", lambda: self.show("feedback")),
            ("Reportes", lambda: self.show("reports")),
        ]

    def show(self, view_name: str) -> None:
        """Render the selected view."""

        view_class = self.views[view_name]
        self.content.show(view_class, on_ready=self._set_current, cache_key=view_name)

    def _set_current(self, view) -> None:
        self.current = view
