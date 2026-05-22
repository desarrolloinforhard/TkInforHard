"""Icon browser showcase view."""

from __future__ import annotations

import importlib
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.layout import IHPage
from TkInforHard.widgets import IHButton, IHImageGridTable, IHSectionHeader


@dataclass(frozen=True)
class IconProviderConfig:
    """Runtime configuration for one ttkbootstrap-icons provider."""

    key: str
    label: str
    package: str
    provider_class: str
    icon_class: str


PROVIDERS = (
    IconProviderConfig(
        key="mat",
        label="Material Design Icons",
        package="ttkbootstrap_icons_mat",
        provider_class="MaterialDesignFontProvider",
        icon_class="MatIcon",
    ),
    IconProviderConfig(
        key="gmi",
        label="Google Material Icons",
        package="ttkbootstrap_icons_gmi",
        provider_class="GoogleMaterialIconFontProvider",
        icon_class="GMatIcon",
    ),
    IconProviderConfig(
        key="fa",
        label="Font Awesome 6 Free",
        package="ttkbootstrap_icons_fa",
        provider_class="FontAwesomeFontProvider",
        icon_class="FAIcon",
    ),
)

COLOR_PRESETS = {
    "Negro": "#111827",
    "Azul": "#0d6efd",
    "Verde": "#009845",
    "Rojo": "#dc3545",
    "Naranja": "#f59e0b",
    "Blanco": "#ffffff",
}

GRID_PALETTE = {
    "light": {
        "icon": "#111827",
        "tile": "#ffffff",
        "hover": "#eef4f0",
        "selected": "#e8f8ee",
        "border": "#d7e3dc",
        "selected_border": "#009845",
    },
    "dark": {
        "icon": "#f3f7fb",
        "tile": "#18231d",
        "hover": "#213126",
        "selected": "#102d1f",
        "border": "#2b3b32",
        "selected_border": "#31c36d",
    },
}


class IconsView(IHPage):
    """Search and preview installed ttkbootstrap-icons providers."""

    def __init__(self, master=None):
        super().__init__(master)
        self.provider_var = tk.StringVar(value=PROVIDERS[0].label)
        self.style_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.size_var = tk.IntVar(value=32)
        self.color_preset_var = tk.StringVar(value="Negro")
        self.color_var = tk.StringVar(value=COLOR_PRESETS[self.color_preset_var.get()])
        self.status_var = tk.StringVar()
        self.detail_name_var = tk.StringVar(value="-")
        self.detail_style_var = tk.StringVar(value="-")
        self.detail_provider_var = tk.StringVar(value="-")
        self.detail_unicode_var = tk.StringVar(value="-")
        self.preview_image = None
        self.providers = self._load_providers()
        self.selected_icon = None
        self.icon_grid = None
        self.color_swatches: dict[str, tk.Label] = {}

        IHSectionHeader(
            self,
            title="Icon Browser",
            subtitle="Buscar, previsualizar y copiar iconos con presets de color.",
        ).pack(fill="x", pady=(0, 14))

        if not self.providers:
            self._build_missing_dependency_state()
            return

        self._build_toolbar()
        self._build_content()
        self.bind("<<IHThemeChanged>>", lambda _event: self._sync_visual_palette())
        self._select_default_provider()

    def _load_providers(self) -> dict[str, dict]:
        loaded = {}
        for config in PROVIDERS:
            try:
                module = importlib.import_module(config.package)
                provider = getattr(module, config.provider_class)()
                icon_class = getattr(module, config.icon_class)
            except Exception:
                continue

            loaded[config.label] = {
                "config": config,
                "provider": provider,
                "icon_class": icon_class,
                "index": provider.build_display_index(),
            }
        return loaded

    def _build_missing_dependency_state(self) -> None:
        frame = ttk.Frame(self, padding=18, style="IH.Surface.TFrame")
        frame.pack(fill="x")
        ttk.Label(
            frame,
            text=(
                "Instala ttkbootstrap-icons y los providers para habilitar el browser:\n"
                "python -m pip install ttkbootstrap-icons ttkbootstrap-icons-mat "
                "ttkbootstrap-icons-gmi ttkbootstrap-icons-fa"
            ),
            style="IH.TLabel",
            justify="left",
        ).pack(anchor="w")

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self, style="IH.Surface.TFrame", padding=12)
        toolbar.pack(fill="x", pady=(0, 12))
        toolbar.columnconfigure(1, weight=1)
        toolbar.columnconfigure(5, weight=1)

        ttk.Label(toolbar, text="Provider", style="IH.TLabel").grid(row=0, column=0, sticky="w")
        provider_box = ttk.Combobox(
            toolbar,
            textvariable=self.provider_var,
            values=list(self.providers.keys()),
            state="readonly",
            width=28,
        )
        provider_box.grid(row=0, column=1, sticky="ew", padx=(8, 14))
        provider_box.bind("<<ComboboxSelected>>", lambda _event: self._on_provider_changed())

        ttk.Label(toolbar, text="Style", style="IH.TLabel").grid(row=0, column=2, sticky="w")
        self.style_box = ttk.Combobox(toolbar, textvariable=self.style_var, state="readonly", width=14)
        self.style_box.grid(row=0, column=3, sticky="w", padx=(8, 14))
        self.style_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh_icons())

        ttk.Label(toolbar, text="Size", style="IH.TLabel").grid(row=0, column=4, sticky="w")
        size_box = ttk.Spinbox(
            toolbar,
            from_=16,
            to=96,
            increment=4,
            textvariable=self.size_var,
            width=6,
            command=self.refresh_icons,
        )
        size_box.grid(row=0, column=5, sticky="w", padx=(8, 14))
        size_box.bind("<Return>", lambda _event: self.refresh_preview())
        size_box.bind("<FocusOut>", lambda _event: self.refresh_preview())

        ttk.Label(toolbar, text="Color", style="IH.TLabel").grid(row=0, column=6, sticky="w")
        color_box = ttk.Combobox(
            toolbar,
            textvariable=self.color_preset_var,
            values=list(COLOR_PRESETS.keys()),
            state="readonly",
            width=10,
        )
        color_box.grid(row=0, column=7, sticky="w", padx=(8, 8))
        color_box.bind("<<ComboboxSelected>>", lambda _event: self._set_color_preset())

        swatches = ttk.Frame(toolbar, style="IH.Surface.TFrame")
        swatches.grid(row=0, column=8, sticky="e")
        for name, color in COLOR_PRESETS.items():
            button = tk.Label(
                swatches,
                background=color,
                width=3,
                height=1,
                cursor="hand2",
                relief="solid",
                borderwidth=2,
            )
            button.bind("<Button-1>", lambda _event, preset=name: self._set_color_preset(preset))
            button.pack(side="left", padx=2)
            self.color_swatches[name] = button
        self._sync_color_swatches()

        ttk.Label(toolbar, text="Buscar", style="IH.TLabel").grid(row=1, column=0, sticky="w", pady=(10, 0))
        search = ttk.Entry(toolbar, textvariable=self.search_var)
        search.grid(row=1, column=1, columnspan=8, sticky="ew", padx=(8, 0), pady=(10, 0))
        search.bind("<KeyRelease>", lambda _event: self.refresh_icons())

    def _build_content(self) -> None:
        body = ttk.Frame(self, style="IH.TFrame")
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, minsize=280)
        body.rowconfigure(0, weight=1)

        self.icon_grid = IHImageGridTable(
            body,
            rows=8,
            columns=10,
            cell_size=50,
            image_factory=self._grid_image_for,
            image_key_getter=self._grid_image_key,
            label_getter=lambda item: item["name"],
            on_select=self.select_icon,
            show_labels=False,
            renderer="canvas",
            cache_images=True,
            **self._grid_palette_args(),
        )
        self.icon_grid.grid(row=0, column=0, sticky="nsew")

        details = ttk.Frame(body, style="IH.Surface.TFrame", padding=14)
        details.grid(row=0, column=1, sticky="nsew", padx=(14, 0))
        details.columnconfigure(0, weight=1)

        ttk.Label(details, text="Preview", style="IH.TLabel").grid(row=0, column=0, sticky="w")
        self.preview_label = ttk.Label(details, text="", anchor="center")
        self.preview_label.grid(row=1, column=0, sticky="ew", pady=(10, 18))

        ttk.Label(details, textvariable=self.detail_name_var, style="IH.TLabel", wraplength=250).grid(
            row=2, column=0, sticky="w"
        )
        ttk.Label(details, textvariable=self.detail_style_var, style="IH.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Label(details, textvariable=self.detail_provider_var, style="IH.TLabel").grid(row=4, column=0, sticky="w")
        ttk.Label(details, textvariable=self.detail_unicode_var, style="IH.TLabel").grid(
            row=5, column=0, sticky="w", pady=(0, 16)
        )
        IHButton(details, text="Copy Name", variant="primary", command=self.copy_selected_name).grid(
            row=6, column=0, sticky="ew"
        )
        ttk.Label(details, textvariable=self.status_var, style="IH.TLabel", wraplength=250).grid(
            row=7, column=0, sticky="ew", pady=(12, 0)
        )

    def _select_default_provider(self) -> None:
        self.provider_var.set(next(iter(self.providers.keys())))
        self._on_provider_changed()

    def _on_provider_changed(self) -> None:
        provider_data = self.providers[self.provider_var.get()]
        styles = provider_data["index"]["styles"] or ("base",)
        self.style_box.configure(values=styles)
        self.style_var.set(provider_data["index"]["default_style"] or styles[0])
        self.refresh_icons()

    def _set_color_preset(self, preset: str | None = None) -> None:
        if preset is not None:
            self.color_preset_var.set(preset)
        self.color_var.set(COLOR_PRESETS[self.color_preset_var.get()])
        self._sync_color_swatches()
        self.refresh_preview()

    def _sync_color_swatches(self) -> None:
        selected = self.color_preset_var.get()
        for name, swatch in self.color_swatches.items():
            is_selected = name == selected
            swatch.configure(
                background=COLOR_PRESETS[name],
                highlightthickness=2 if is_selected else 1,
                highlightbackground="#31c36d" if is_selected else "#6b7280",
                highlightcolor="#31c36d" if is_selected else "#6b7280",
                relief="solid",
            )

    def refresh_icons(self) -> None:
        if self.icon_grid is None:
            return

        icons = self._filtered_icons()
        self.status_var.set(f"{len(icons)} icons")
        self.icon_grid.load(icons)
        if not icons:
            self.selected_icon = None
            self.preview_label.configure(image="", text="No icons")
            self.detail_name_var.set("Name: -")
            self.detail_style_var.set("Style: -")
            self.detail_provider_var.set("Provider: -")
            self.detail_unicode_var.set("Unicode: -")

    def _filtered_icons(self) -> list[dict[str, str]]:
        provider_data = self.providers[self.provider_var.get()]
        provider = provider_data["provider"]
        style = self.style_var.get() or provider_data["index"]["default_style"] or "base"
        names_by_style = provider_data["index"]["names_by_style"]
        names = list(names_by_style.get(style, names_by_style.get("base", {})).keys())
        term = self.search_var.get().strip().lower()
        if term:
            names = [name for name in names if term in name.lower()]
        return [
            {
                "name": name,
                "style": style,
                "provider": provider.display_name,
                "unicode": self._unicode_for(name, style),
            }
            for name in names
        ]

    def select_icon(self, item: dict[str, str]) -> None:
        self.selected_icon = item
        name = item["name"]
        style = item["style"]
        provider_data = self.providers[self.provider_var.get()]
        self.preview_image = self._create_icon_image(name, size=max(64, self.size_var.get() * 2))
        self.preview_label.configure(image=self.preview_image, text="")
        self.detail_name_var.set(f"Name: {name}")
        self.detail_style_var.set(f"Style: {style}")
        self.detail_provider_var.set(f"Provider: {item['provider']}")
        self.detail_unicode_var.set(f"Unicode: {item['unicode']}")

    def refresh_preview(self) -> None:
        if self.selected_icon is not None:
            self.select_icon(self.selected_icon)
        if self.icon_grid is not None:
            self.icon_grid.refresh_images()

    def _grid_image_for(self, item: dict[str, str], size: int | None = None):
        return self._create_icon_image(item["name"], size=size or self.size_var.get(), color=self._grid_icon_color())

    def _grid_image_key(self, item: dict[str, str]) -> str:
        return "|".join(
            (
                item["provider"],
                item["style"],
                item["name"],
                str(self.size_var.get()),
                self._grid_icon_color(),
            )
        )

    def _create_icon_image(self, name: str, size: int, color: str | None = None):
        provider_data = self.providers[self.provider_var.get()]
        icon_class = provider_data["icon_class"]
        style = self.style_var.get() or None
        try:
            return icon_class(name, size=max(16, int(size)), color=color or self.color_var.get(), style=style).image
        except Exception:
            return tk.PhotoImage(width=max(16, int(size)), height=max(16, int(size)))

    def _sync_visual_palette(self) -> None:
        if self.icon_grid is not None:
            self.icon_grid.configure_palette(**self._grid_palette_args())
        self.refresh_preview()

    def _grid_palette_args(self) -> dict[str, str]:
        palette = GRID_PALETTE[self._visual_mode()]
        return {
            "tile_background": palette["tile"],
            "tile_hover_background": palette["hover"],
            "tile_selected_background": palette["selected"],
            "tile_border": palette["border"],
            "tile_selected_border": palette["selected_border"],
        }

    def _grid_icon_color(self) -> str:
        return GRID_PALETTE[self._visual_mode()]["icon"]

    def _visual_mode(self) -> str:
        try:
            theme_name = self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            theme_name = ""
        return "light" if "light" in str(theme_name).lower() else "dark"

    def _unicode_for(self, name: str, style: str | None) -> str:
        provider = self.providers[self.provider_var.get()]["provider"]
        try:
            resolved = provider.resolve_icon_name(name, style)
            glyphmap = provider._read_glyphmap_for_style(style)
            value = glyphmap.get(resolved)
            if value is None:
                return "-"
            return f"U+{str(value).upper()}"
        except Exception:
            return "-"

    def copy_selected_name(self) -> None:
        if self.selected_icon is None:
            messagebox.showinfo("Icon Browser", "Selecciona un icono primero.")
            return
        selected_name = self.selected_icon["name"]
        self.clipboard_clear()
        self.clipboard_append(selected_name)
        self.status_var.set(f"Copied: {selected_name}")
