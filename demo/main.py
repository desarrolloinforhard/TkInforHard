"""TkInforHard showcase application."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from TkInforHard.core import IHApplication, IHConfig
from TkInforHard.widgets import IHSidebar, IHTopbar
from demo.controllers.showcase_controller import ShowcaseController


def main() -> None:
    """Run the component showcase."""

    app = IHApplication(IHConfig(title="TkInforHard Showcase", width=1280, height=820))
    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=1)

    controller = ShowcaseController(app)
    sidebar = IHSidebar(app, title="TkInforHard", items=controller.menu_items())
    sidebar.grid(row=0, column=0, rowspan=2, sticky="nsw")

    topbar = IHTopbar(app, title="Component Showcase", on_toggle_theme=app.toggle_theme)
    topbar.grid(row=0, column=1, sticky="ew")

    controller.content.grid(row=1, column=1, sticky="nsew")
    controller.show("showcase")
    app.mainloop()


if __name__ == "__main__":
    main()

