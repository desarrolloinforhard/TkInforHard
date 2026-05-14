"""Controller for the demo showcase views."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from demo.views.buttons_view import ButtonsView
from demo.views.cards_view import CardsView
from demo.views.feedback_view import FeedbackView
from demo.views.inputs_view import InputsView
from demo.views.showcase_view import ShowcaseView
from demo.views.tables_view import TablesView


class ShowcaseController:
    """Coordinates view navigation for the demo without defining UI components."""

    def __init__(self, master):
        self.content = ttk.Frame(master, style="IH.TFrame")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)
        self.views = {
            "showcase": ShowcaseView,
            "buttons": ButtonsView,
            "cards": CardsView,
            "inputs": InputsView,
            "tables": TablesView,
            "feedback": FeedbackView,
        }
        self.current = None

    def menu_items(self) -> list[tuple[str, object]]:
        """Return sidebar menu items."""

        return [
            ("Showcase", lambda: self.show("showcase")),
            ("Buttons", lambda: self.show("buttons")),
            ("Cards", lambda: self.show("cards")),
            ("Inputs", lambda: self.show("inputs")),
            ("Tables", lambda: self.show("tables")),
            ("Feedback", lambda: self.show("feedback")),
        ]

    def show(self, view_name: str) -> None:
        """Render the selected view."""

        if self.current is not None:
            self.current.destroy()
        self.current = self.views[view_name](self.content)
        self.current.grid(row=0, column=0, sticky="nsew")

