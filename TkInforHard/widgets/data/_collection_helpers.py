"""Internal helpers for collection-style data widgets."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.core.constants import DARK_THEME, LIGHT_THEME
from TkInforHard.theme.tokens import get_tokens


SEMANTIC_VARIANTS = {"info", "success", "warning", "danger", "muted"}


def current_tokens() -> dict:
    """Return tokens that match the active ttk theme when possible."""

    try:
        theme_name = ttk.Style().theme_use()
    except Exception:
        theme_name = DARK_THEME
    if theme_name == LIGHT_THEME or "light" in theme_name or theme_name == "flatly":
        return get_tokens(LIGHT_THEME)
    return get_tokens(DARK_THEME)


def variant_color(tokens: dict, variant: str | None) -> str:
    """Resolve a semantic variant into a token color."""

    color = tokens["color"]
    if variant in {"success", "info", "warning", "danger"}:
        return color[variant]
    if variant == "muted":
        return color["muted"]
    return color["info"]


def format_datetime(value: Any) -> str:
    """Format date-like values without imposing a business-specific format."""

    if value in (None, ""):
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return str(value)


def sort_datetime_value(value: Any) -> Any:
    """Return a stable sort key for mixed datetime/string values."""

    if isinstance(value, (datetime, date)):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return value
    return value or ""


def metadata_text(metadata: dict | None) -> str:
    """Render optional metadata as compact key/value text."""

    if not metadata:
        return ""
    return "   ".join(f"{key}: {value}" for key, value in metadata.items())
