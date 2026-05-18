"""Table component."""

from __future__ import annotations

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

_TAGS_LIGHT = {
    "green":  {"background": "#d4edda", "foreground": "#155724"},
    "yellow": {"background": "#fff3cd", "foreground": "#856404"},
    "red":    {"background": "#f8d7da", "foreground": "#721c24"},
}

_TAGS_DARK = {
    "green":  {"background": "#0D3320", "foreground": "#FFFFFF"},
    "yellow": {"background": "#3D2B00", "foreground": "#FFFFFF"},
    "red":    {"background": "#3A1D23", "foreground": "#FFFFFF"},
}


class IHTable(ttk.Frame):
    """Reusable Treeview table with a small data-loading API.

    Parameters
    ----------
    row_tag_key : str | None
        When set and rows are dicts, the value at this key is used as the
        Treeview tag for that row, enabling per-row background colors.

    Methods
    -------
    load(rows)
        Replace table rows. Accepts list[tuple] (original) or list[dict]
        when row_tag_key is set.
    set_tag_color(tag, background, fg=None)
        Configure custom colors for a tag name.
    """

    def __init__(
        self,
        master=None,
        columns: list[str] | tuple[str, ...] = (),
        rows: list[tuple] | None = None,
        row_tag_key: str | None = None,
        **kwargs,
    ):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self._row_tag_key = row_tag_key
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="IH.Treeview")
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=140, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self._apply_default_tags()
        self.load(rows or [])
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")

    # ── Public ────────────────────────────────────────────────────────────────

    def load(self, rows: list) -> None:
        """Replace table rows."""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            if self._row_tag_key and isinstance(row, dict):
                tag = row.get(self._row_tag_key, "")
                values = tuple(v for k, v in row.items() if k != self._row_tag_key)
                self.tree.insert("", "end", values=values, tags=(tag,))
            else:
                self.tree.insert("", "end", values=row)

    def set_tag_color(self, tag: str, background: str, fg: str | None = None) -> None:
        """Configure custom colors for a tag."""

        opts: dict = {"background": background}
        if fg is not None:
            opts["foreground"] = fg
        self.tree.tag_configure(tag, **opts)

    # ── Private ───────────────────────────────────────────────────────────────

    def _apply_default_tags(self) -> None:
        try:
            theme = self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            theme = "inforhard_dark"
        tag_map = _TAGS_DARK if theme == "inforhard_dark" else _TAGS_LIGHT
        for tag_name, colors in tag_map.items():
            self.tree.tag_configure(tag_name, **colors)

    def _on_theme_changed(self, _event=None) -> None:
        self._apply_default_tags()
