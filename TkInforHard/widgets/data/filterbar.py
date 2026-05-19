"""Filter bar component."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.buttons.button import IHButton
from TkInforHard.widgets.inputs.date_input import IHDateInput
from TkInforHard.widgets.inputs.search_input import IHSearchInput


class IHFilterBar(ttk.Frame):
    """Horizontal filter area with search and refresh actions.

    Modo simple (sin fields):
        IHFilterBar(master, on_search=..., on_refresh=...)
        Muestra IHSearchInput + botones "Buscar" / "Actualizar".

    Modo declarativo (con fields):
        IHFilterBar(master, fields=[...])
        Acepta una lista de dicts con los tipos: date, combo, button.

        Ejemplo:
            fields=[
                {"type": "date",   "key": "desde",   "label": "Desde"},
                {"type": "date",   "key": "hasta",   "label": "Hasta"},
                {"type": "combo",  "key": "suc",     "label": "Sucursal",
                 "values": ["(Todas)"]},
                {"type": "button", "key": "generar", "label": "Generar",
                 "variant": "primary", "command": None, "state": "normal"},
                {"type": "button", "key": "csv",     "label": "CSV",
                 "variant": "success", "outline": True, "state": "disabled"},
            ]

    Métodos públicos (modo declarativo):
        get_values()                 -> dict[key, str]
        set_state(key, state)        state: "normal" | "disabled"
        update_combo(key, values)
    """

    def __init__(
        self,
        master=None,
        on_search=None,
        on_refresh=None,
        fields: list[dict] | None = None,
        **kwargs,
    ):
        super().__init__(master, padding=(0, 0, 0, 12), style="IH.Surface.TFrame", **kwargs)
        self._fields = fields
        self._vars: dict[str, tk.StringVar] = {}
        self._widgets: dict[str, object] = {}

        if fields is None:
            self._build_simple(on_search, on_refresh)
        else:
            self._build_declarative(fields)

    # ── Simple mode ───────────────────────────────────────────────────────────

    def _build_simple(self, on_search, on_refresh) -> None:
        self.search = IHSearchInput(self)
        self.search.pack(side="left", fill="x", expand=True)
        IHButton(self, text="Buscar", variant="success", command=on_search).pack(
            side="left", padx=(8, 0)
        )
        IHButton(self, text="Actualizar", variant="secondary", outline=True, command=on_refresh).pack(
            side="left", padx=(8, 0)
        )

    # ── Declarative mode ──────────────────────────────────────────────────────

    def _build_declarative(self, fields: list[dict]) -> None:
        for field in fields:
            ftype = field.get("type")
            key = field.get("key", "")
            label = field.get("label", "")

            if ftype == "date":
                from ttkbootstrap.widgets import DateEntry
                from datetime import datetime
                if label:
                    ttk.Label(self, text=label + ":").pack(side="left", padx=(8, 2))
                entry = DateEntry(
                    self,
                    dateformat="%Y-%m-%d",
                    firstweekday=0,
                    startdate=datetime.today(),
                    bootstyle="success",
                    width=10,
                )
                entry.pack(side="left", padx=(0, 4))
                self._widgets[key] = entry

            elif ftype == "combo":
                var = tk.StringVar()
                self._vars[key] = var
                values = field.get("values", [])
                container = ttk.Frame(self, style="IH.Surface.TFrame")
                container.pack(side="left", padx=(0, 8))
                ttk.Label(container, text=label, style="IH.Surface.TLabel").pack(anchor="w")
                cb = ttk.Combobox(container, textvariable=var, values=values, width=14)
                if values:
                    cb.set(values[0])
                cb.pack()
                self._widgets[key] = cb

            elif ftype == "button":
                variant = field.get("variant", "primary")
                outline = field.get("outline", False)
                command = field.get("command")
                state = field.get("state", "normal")
                btn = IHButton(
                    self,
                    text=label,
                    variant=variant,
                    outline=outline,
                    command=command,
                    state=state,
                )
                btn.pack(side="left", padx=(0, 8), pady=(14, 0))
                self._widgets[key] = btn

    # ── Public API (declarative mode) ─────────────────────────────────────────

    def get_values(self) -> dict:
        """Return current values for all date and combo fields."""

        values = {}
        for key, widget in self._widgets.items():
            if isinstance(widget, IHButton):
                continue
            if hasattr(widget, "entry"):
                values[key] = widget.entry.get()
            else:
                try:
                    values[key] = widget.get()
                except Exception:
                    pass
        return values

    def set_state(self, key: str, state: str) -> None:
        """Set the state of a button or input by key."""

        widget = self._widgets.get(key)
        if widget is None:
            return
        try:
            widget.configure(state=state)
        except Exception:
            pass

    def update_combo(self, key: str, values: list) -> None:
        """Replace the values list of a combo field."""

        widget = self._widgets.get(key)
        if widget is None:
            return
        try:
            widget.configure(values=values)
            if values:
                widget.set(values[0])
        except Exception:
            pass
