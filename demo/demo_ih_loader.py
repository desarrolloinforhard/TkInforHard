"""Standalone demo for the corporate IHLoader component."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.components import IHLoader
from TkInforHard.core import IHApplication, IHConfig


def main() -> None:
    """Run a simple loader gallery."""

    app = IHApplication(IHConfig(title="IHLoader Demo", width=520, height=280))
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)

    frame = ttk.Frame(app, padding=24, style="IH.TFrame")
    frame.grid(row=0, column=0, sticky="nsew")
    ttk.Label(frame, text="IHLoader", style="IH.Title.TLabel").pack(anchor="w")
    ttk.Label(frame, text="Loader corporativo circular sin imagenes externas.", style="IH.Muted.TLabel").pack(
        anchor="w", pady=(4, 18)
    )

    row = ttk.Frame(frame, style="IH.TFrame")
    row.pack(fill="x")
    loaders = []
    for size in (32, 48, 64, 96):
        box = ttk.Frame(row, padding=12, style="IH.Surface.TFrame")
        box.pack(side="left", padx=(0, 12))
        loader = IHLoader(box, size=size, mode="dark", background=app.theme_manager.tokens()["color"]["surface"])
        loader.pack()
        ttk.Label(box, text=f"{size}x{size}", style="IH.Surface.TLabel").pack(pady=(8, 0))
        loader.start()
        loaders.append(loader)

    def toggle_theme() -> None:
        theme = app.toggle_theme()
        mode = "light" if "light" in theme else "dark"
        surface = app.theme_manager.tokens()["color"]["surface"]
        for loader in loaders:
            loader.background = surface
            loader.set_theme(mode)

    ttk.Button(frame, text="Cambiar tema", command=toggle_theme, bootstyle="success-outline").pack(
        anchor="e", pady=(18, 0)
    )
    app.mainloop()


if __name__ == "__main__":
    main()
