"""Centralized ttk style registration."""

from __future__ import annotations

from TkInforHard.theme.tokens import get_tokens


def register_styles(style, theme_name: str) -> None:
    """Configure TkInforHard style names for the current ttk style object."""

    tokens = get_tokens(theme_name)
    color = tokens["color"]
    navigation = tokens["navigation"]
    font = tokens["font"]
    body_font = (font["family"], font["body"])
    title_font = (font["family"], font["title"], font["bold"])
    small_font = (font["family"], font["small"])

    style.configure(".", font=body_font)
    style.configure("IH.TFrame", background=color["background"])
    style.configure("IH.Surface.TFrame", background=color["surface"])
    style.configure("IH.Card.TFrame", background=color["surface"], relief="flat", borderwidth=1)
    style.configure("IH.Sidebar.TFrame", background=navigation["sidebar_bg"])
    style.configure("IH.Topbar.TFrame", background=color["surface"])

    style.configure("IH.TLabel", background=color["background"], foreground=color["text"], font=body_font)
    style.configure("IH.Surface.TLabel", background=color["surface"], foreground=color["text"], font=body_font)
    style.configure("IH.Title.TLabel", background=color["background"], foreground=color["text"], font=title_font)
    style.configure("IH.Muted.TLabel", background=color["background"], foreground=color["muted"], font=small_font)
    style.configure("IH.CardTitle.TLabel", background=color["surface"], foreground=color["text"], font=title_font)
    style.configure("IH.CardMuted.TLabel", background=color["surface"], foreground=color["muted"], font=small_font)
    style.configure("IH.SidebarTitle.TLabel", background=navigation["sidebar_bg"], foreground=navigation["brand"], font=title_font)

    style.configure("IH.TEntry", fieldbackground=color["surface_alt"], foreground=color["text"])
    style.configure("IH.TCombobox", fieldbackground=color["surface_alt"], foreground=color["text"])
    style.configure("IH.Treeview", rowheight=34, font=body_font)
    style.configure("IH.Treeview.Heading", font=(font["family"], font["body"], font["bold"]))

    for variant in ("primary", "secondary", "success", "info", "warning", "danger", "light", "dark"):
        style.configure(f"IH.{variant}.TButton", padding=(14, 9), font=body_font)
        style.configure(f"IH.outline-{variant}.TButton", padding=(14, 9), font=body_font)
        style.configure(f"IH.{variant}.Toolbutton", padding=(10, 8), font=body_font)
