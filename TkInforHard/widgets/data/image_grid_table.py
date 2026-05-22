"""Paginated image grid table component."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable, Sequence
from typing import Any

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHImageGridTable(ttk.Frame):
    """Reusable paginated grid for image-based records."""

    def __init__(
        self,
        master=None,
        items: Sequence[Any] | None = None,
        image_factory: Callable[[Any], object] | None = None,
        label_getter: Callable[[Any], str] | None = None,
        image_key_getter: Callable[[Any], str] | None = None,
        on_select: Callable[[Any], None] | None = None,
        rows: int = 8,
        columns: int = 8,
        max_rows: int = 10,
        max_columns: int = 10,
        cell_size: int = 52,
        show_labels: bool = False,
        empty_text: str = "Sin resultados",
        tile_background: str = "#ffffff",
        tile_hover_background: str = "#f1f5f9",
        tile_selected_background: str = "#ecfdf5",
        tile_border: str = "#d7e3dc",
        tile_selected_border: str = "#009845",
        renderer: str = "canvas",
        cache_images: bool = True,
        max_cached_images: int = 1000,
        **kwargs,
    ):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self.rows = self._clamp(rows, 1, max_rows)
        self.columns = self._clamp(columns, 1, max_columns)
        self.max_rows = max_rows
        self.max_columns = max_columns
        self.cell_size = max(32, cell_size)
        self.show_labels = show_labels
        self.empty_text = empty_text
        self.tile_background = tile_background
        self.tile_hover_background = tile_hover_background
        self.tile_selected_background = tile_selected_background
        self.tile_border = tile_border
        self.tile_selected_border = tile_selected_border
        self.image_factory = image_factory
        self.label_getter = label_getter or (lambda item: str(item))
        self.image_key_getter = image_key_getter or (lambda item: str(item))
        self.on_select = on_select
        self.renderer = renderer
        self.cache_images = cache_images
        self.max_cached_images = max_cached_images
        self.items = list(items or [])
        self.page = 0
        self.selected_item = None
        self._images: list[object] = []
        self._image_cache: dict[str, object] = {}
        self._image_cache_order: list[str] = []
        self._tiles: dict[int, tuple[tk.Frame, tk.Frame, tk.Label]] = {}
        self._canvas_items: list[dict[str, int]] = []

        self.grid_container = ttk.Frame(self, style="IH.TFrame")
        self.grid_container.pack(fill="both", expand=True, padx=10, pady=10)
        if self.renderer == "canvas":
            self.grid_canvas = tk.Canvas(self.grid_container, highlightthickness=0, borderwidth=0)
            self.grid_canvas.pack(fill="both", expand=True)
            self.grid_canvas.bind("<Configure>", lambda _event: self.render(keep_selection=True))
            self.grid_frame = None
        else:
            self.grid_canvas = None
            self.grid_frame = ttk.Frame(self.grid_container, style="IH.TFrame")
            self.grid_frame.pack(fill="both", expand=True)

        self.footer = ttk.Frame(self, style="IH.Surface.TFrame")
        self.footer.pack(fill="x", padx=8, pady=(0, 8))
        self.previous_button = ttk.Button(self.footer, text="Anterior", command=self.previous_page)
        self.previous_button.pack(side="left")
        self.status_var = tk.StringVar()
        ttk.Label(self.footer, textvariable=self.status_var, style="IH.TLabel").pack(side="left", padx=12)
        self.next_button = ttk.Button(self.footer, text="Siguiente", command=self.next_page)
        self.next_button.pack(side="left")

        self.render()

    @property
    def page_size(self) -> int:
        """Return the number of records shown per page."""

        return self.rows * self.columns

    def load(self, items: Sequence[Any], reset_page: bool = True) -> None:
        """Replace all records and render the current page."""

        self.items = list(items)
        if reset_page:
            self.page = 0
        self.selected_item = None
        self.render()

    def refresh_images(self) -> None:
        """Re-render the current page using the existing data."""

        self.render(keep_selection=True)

    def configure_palette(
        self,
        tile_background: str,
        tile_hover_background: str,
        tile_selected_background: str,
        tile_border: str,
        tile_selected_border: str,
    ) -> None:
        """Update tile colors and re-render."""

        self.tile_background = tile_background
        self.tile_hover_background = tile_hover_background
        self.tile_selected_background = tile_selected_background
        self.tile_border = tile_border
        self.tile_selected_border = tile_selected_border
        self.render(keep_selection=True)

    def next_page(self) -> None:
        """Move to the next page when available."""

        if (self.page + 1) * self.page_size < len(self.items):
            self.page += 1
            self.render()

    def previous_page(self) -> None:
        """Move to the previous page when available."""

        if self.page > 0:
            self.page -= 1
            self.render()

    def render(self, keep_selection: bool = False) -> None:
        """Render the visible grid page."""

        if self.renderer == "canvas":
            self._render_canvas(keep_selection=keep_selection)
            return

        page_items = self._page_items()
        if not keep_selection:
            self.selected_item = None

        next_frame = ttk.Frame(self.grid_container, style="IH.TFrame")
        next_images: list[object] = []
        next_tiles: dict[int, tuple[tk.Frame, tk.Frame, tk.Label]] = {}

        for row in range(self.rows):
            next_frame.rowconfigure(row, weight=1, minsize=self.cell_size)
        for column in range(self.columns):
            next_frame.columnconfigure(column, weight=1, minsize=self.cell_size)

        if not page_items:
            ttk.Label(next_frame, text=self.empty_text, style="IH.TLabel").grid(
                row=0, column=0, columnspan=self.columns, sticky="nsew", pady=24
            )
            self._swap_grid_frame(next_frame, next_images, next_tiles)
            self._update_status()
            return

        for index, item in enumerate(page_items):
            row, column = divmod(index, self.columns)
            image = self._make_image(item)
            next_images.append(image)
            text = self.label_getter(item) if self.show_labels else ""
            tile = self._build_tile(next_frame, next_tiles, item, image, text)
            tile.grid(row=row, column=column, sticky="nsew", padx=4, pady=4)

        self._swap_grid_frame(next_frame, next_images, next_tiles)
        if self.selected_item in page_items:
            self.select(self.selected_item)
        elif page_items:
            self.select(page_items[0])
        self._update_status()

    def select(self, item: Any) -> None:
        """Select one item and notify listeners."""

        self.selected_item = item
        if self.renderer == "canvas":
            self._sync_canvas_states()
        else:
            self._sync_tile_states()
        if self.on_select is not None:
            self.on_select(item)

    def _render_canvas(self, keep_selection: bool = False) -> None:
        if self.grid_canvas is None:
            return
        if not keep_selection:
            self.selected_item = None

        page_items = self._page_items()
        self._ensure_canvas_cells()
        self._images.clear()

        canvas_width = max(1, self.grid_canvas.winfo_width())
        canvas_height = max(1, self.grid_canvas.winfo_height())
        gap = 7
        available_width = max(1, canvas_width - gap * (self.columns + 1))
        available_height = max(1, canvas_height - gap * (self.rows + 1))
        cell_width = max(32, available_width // self.columns)
        cell_height = max(32, available_height // self.rows)
        icon_size = min(self.cell_size, cell_width - 16, cell_height - 16)
        icon_size = max(16, icon_size)

        if not page_items:
            self.grid_canvas.delete("empty")
            self.grid_canvas.create_text(
                canvas_width // 2,
                canvas_height // 2,
                text=self.empty_text,
                fill=self.tile_selected_border,
                tags=("empty",),
            )
            self._hide_all_canvas_cells()
            self._update_status()
            return
        self.grid_canvas.delete("empty")

        for index, cell in enumerate(self._canvas_items):
            if index >= len(page_items):
                self._configure_canvas_cell(cell, state="hidden")
                continue

            item = page_items[index]
            row, column = divmod(index, self.columns)
            x1 = gap + column * (cell_width + gap)
            y1 = gap + row * (cell_height + gap)
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            cx = x1 + cell_width // 2
            cy = y1 + cell_height // 2
            image = self._make_image(item, image_size=icon_size)
            self._images.append(image)
            self.grid_canvas.coords(cell["rect"], x1, y1, x2, y2)
            self.grid_canvas.coords(cell["image"], cx, cy)
            self.grid_canvas.itemconfigure(cell["image"], image=image)
            if self.show_labels:
                self.grid_canvas.coords(cell["text"], cx, y2 - 10)
                self.grid_canvas.itemconfigure(cell["text"], text=self.label_getter(item))
            else:
                self.grid_canvas.itemconfigure(cell["text"], text="")
            cell["item"] = item
            self._configure_canvas_cell(cell, state="normal")

        if self.selected_item in page_items:
            self.select(self.selected_item)
        else:
            self.select(page_items[0])
        self._update_status()

    def _ensure_canvas_cells(self) -> None:
        if self.grid_canvas is None or self._canvas_items:
            return
        for index in range(self.page_size):
            tag = f"cell_{index}"
            rect = self.grid_canvas.create_rectangle(
                0,
                0,
                1,
                1,
                fill=self.tile_background,
                outline=self.tile_border,
                width=1,
                tags=(tag, "cell"),
            )
            image = self.grid_canvas.create_image(0, 0, tags=(tag, "cell"))
            text = self.grid_canvas.create_text(0, 0, fill=self.tile_selected_border, font=("Segoe UI", 8), tags=(tag, "cell"))
            cell = {"rect": rect, "image": image, "text": text, "item": None}
            self._canvas_items.append(cell)
            self.grid_canvas.tag_bind(tag, "<Button-1>", lambda _event, i=index: self._select_canvas_index(i))
            self.grid_canvas.tag_bind(tag, "<Enter>", lambda _event, i=index: self._hover_canvas_index(i, True))
            self.grid_canvas.tag_bind(tag, "<Leave>", lambda _event, i=index: self._hover_canvas_index(i, False))

    def _select_canvas_index(self, index: int) -> None:
        if index >= len(self._canvas_items):
            return
        item = self._canvas_items[index].get("item")
        if item is not None:
            self.select(item)

    def _hover_canvas_index(self, index: int, hover: bool) -> None:
        if index >= len(self._canvas_items):
            return
        cell = self._canvas_items[index]
        item = cell.get("item")
        if item is None or item == self.selected_item or self.grid_canvas is None:
            return
        self.grid_canvas.itemconfigure(
            cell["rect"],
            fill=self.tile_hover_background if hover else self.tile_background,
        )

    def _hide_all_canvas_cells(self) -> None:
        for cell in self._canvas_items:
            self._configure_canvas_cell(cell, state="hidden")

    def _configure_canvas_cell(self, cell: dict[str, int], state: str) -> None:
        if self.grid_canvas is None:
            return
        self.grid_canvas.itemconfigure(cell["rect"], state=state)
        self.grid_canvas.itemconfigure(cell["image"], state=state)
        self.grid_canvas.itemconfigure(cell["text"], state=state)

    def _sync_canvas_states(self) -> None:
        if self.grid_canvas is None:
            return
        for cell in self._canvas_items:
            item = cell.get("item")
            if item is None:
                continue
            selected = item == self.selected_item
            self.grid_canvas.itemconfigure(
                cell["rect"],
                fill=self.tile_selected_background if selected else self.tile_background,
                outline=self.tile_selected_border if selected else self.tile_border,
                width=2 if selected else 1,
            )

    def _swap_grid_frame(
        self,
        next_frame,
        next_images: list[object],
        next_tiles: dict[int, tuple[tk.Frame, tk.Frame, tk.Label]],
    ) -> None:
        current_frame = self.grid_frame
        self.grid_frame = next_frame
        self._images = next_images
        self._tiles = next_tiles
        current_frame.pack_forget()
        next_frame.pack(fill="both", expand=True)
        current_frame.destroy()

    def _build_tile(
        self,
        parent,
        tiles: dict[int, tuple[tk.Frame, tk.Frame, tk.Label]],
        item: Any,
        image: object,
        text: str,
    ) -> tk.Frame:
        outer = tk.Frame(
            parent,
            background=self.tile_border,
            highlightthickness=0,
            borderwidth=0,
            cursor="hand2",
        )
        inner = tk.Frame(outer, background=self.tile_background, borderwidth=0, cursor="hand2")
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        label = tk.Label(
            inner,
            image=image,
            text=text,
            compound="top",
            background=self.tile_background,
            borderwidth=0,
            cursor="hand2",
        )
        label.pack(fill="both", expand=True, padx=8, pady=8)
        if self.show_labels:
            label.configure(wraplength=max(40, self.cell_size - 8), font=("Segoe UI", 8))

        key = id(item)
        tiles[key] = (outer, inner, label)
        for widget in (outer, inner, label):
            widget.bind("<Button-1>", lambda _event, value=item: self.select(value))
            widget.bind("<Enter>", lambda _event, value=item: self._set_tile_hover(value, True))
            widget.bind("<Leave>", lambda _event, value=item: self._set_tile_hover(value, False))
        return outer

    def _set_tile_hover(self, item: Any, hover: bool) -> None:
        if item == self.selected_item:
            return
        tile = self._tiles.get(id(item))
        if tile is None:
            return
        outer, inner, label = tile
        background = self.tile_hover_background if hover else self.tile_background
        outer.configure(background=self.tile_border)
        inner.configure(background=background)
        label.configure(background=background)

    def _sync_tile_states(self) -> None:
        for item in self._page_items():
            tile = self._tiles.get(id(item))
            if tile is None:
                continue
            outer, inner, label = tile
            selected = item == self.selected_item
            outer.configure(background=self.tile_selected_border if selected else self.tile_border)
            inner.configure(background=self.tile_selected_background if selected else self.tile_background)
            label.configure(background=self.tile_selected_background if selected else self.tile_background)

    def _page_items(self) -> list[Any]:
        start = self.page * self.page_size
        end = start + self.page_size
        return self.items[start:end]

    def _make_image(self, item: Any, image_size: int | None = None) -> object:
        cache_key = self.image_key_getter(item)
        if image_size is not None:
            cache_key = f"{cache_key}|{image_size}"
        if self.cache_images and cache_key in self._image_cache:
            return self._image_cache[cache_key]

        if self.image_factory is None:
            image = tk.PhotoImage(width=image_size or self.cell_size, height=image_size or self.cell_size)
        else:
            try:
                if image_size is None:
                    image = self.image_factory(item)
                else:
                    image = self.image_factory(item, image_size)
            except TypeError:
                try:
                    image = self.image_factory(item)
                except Exception:
                    image = tk.PhotoImage(width=image_size or self.cell_size, height=image_size or self.cell_size)
            except Exception:
                image = tk.PhotoImage(width=image_size or self.cell_size, height=image_size or self.cell_size)

        if self.cache_images:
            self._image_cache[cache_key] = image
            self._image_cache_order.append(cache_key)
            while len(self._image_cache_order) > self.max_cached_images:
                old_key = self._image_cache_order.pop(0)
                if old_key not in self._image_cache_order:
                    self._image_cache.pop(old_key, None)
        return image

    def _update_status(self) -> None:
        total = len(self.items)
        if total == 0:
            self.status_var.set("0 resultados")
        else:
            start = self.page * self.page_size + 1
            end = min((self.page + 1) * self.page_size, total)
            self.status_var.set(f"{start}-{end} de {total}")
        self.previous_button.configure(state="normal" if self.page > 0 else "disabled")
        has_next = (self.page + 1) * self.page_size < total
        self.next_button.configure(state="normal" if has_next else "disabled")

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, int(value)))
