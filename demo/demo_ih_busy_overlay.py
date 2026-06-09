"""Standalone demo for IHBusyOverlay."""

from pathlib import Path
import sys
import time
from tkinter import messagebox

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.components import IHBusyOverlay
from TkInforHard.core import IHApplication, IHConfig


def main() -> None:
    """Run a simple busy overlay demo."""

    app = IHApplication(IHConfig(title="IHBusyOverlay Demo", width=560, height=320))
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)

    frame = ttk.Frame(app, padding=24, style="IH.TFrame")
    frame.grid(row=0, column=0, sticky="nsew")
    ttk.Label(frame, text="IHBusyOverlay", style="IH.Title.TLabel").pack(anchor="w")
    ttk.Label(
        frame,
        text="Overlay reusable para procesos largos dentro de una pantalla.",
        style="IH.Muted.TLabel",
    ).pack(anchor="w", pady=(4, 18))

    result_label = ttk.Label(frame, text="Resultado pendiente", style="IH.TLabel")
    result_label.pack(anchor="w", pady=(0, 18))

    overlay = IHBusyOverlay(
        app,
        text="Generando reporte...",
        subtext="Esto puede tardar unos segundos",
        block_input=True,
        min_visible_ms=900,
    )

    def generate_report():
        time.sleep(1.4)
        return "Reporte generado correctamente"

    def run_overlay() -> None:
        overlay.run(
            task=generate_report,
            on_success=lambda result: result_label.configure(text=result),
            on_error=lambda exc: messagebox.showerror("Error", str(exc)),
        )

    ttk.Button(frame, text="Simular proceso largo", command=run_overlay, bootstyle="success").pack(anchor="w")
    app.mainloop()


if __name__ == "__main__":
    main()
