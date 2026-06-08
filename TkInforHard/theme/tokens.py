"""Composed design tokens for light and dark modes."""

from __future__ import annotations

from copy import deepcopy

from TkInforHard.theme import palette, radius, spacing, typography


TOKENS = {
    "inforhard_dark": {
        "color": {
            "primary": palette.DARK_PRIMARY,
            "primary_hover": palette.DARK_PRIMARY_HOVER,
            "background": palette.DARK_BACKGROUND,
            "surface": palette.DARK_SURFACE,
            "surface_alt": palette.DARK_SURFACE_ALT,
            "border": palette.DARK_BORDER,
            "text": palette.DARK_TEXT,
            "muted": palette.DARK_MUTED,
            "success": palette.SUCCESS,
            "info": palette.INFO,
            "warning": palette.DARK_WARNING,
            "danger": palette.DARK_DANGER,
            "topbar_button": palette.DARK_PRIMARY,
            "topbar": palette.DARK_SURFACE,
        },
        "font": {
            "family": typography.FONT_FAMILY,
            "body": typography.FONT_SIZE_MD,
            "small": typography.FONT_SIZE_SM,
            "title": typography.FONT_SIZE_XL,
            "headline": typography.FONT_SIZE_2XL,
            "bold": typography.FONT_WEIGHT_BOLD,
        },
        "spacing": {
            "xs": spacing.SPACE_1,
            "sm": spacing.SPACE_2,
            "md": spacing.SPACE_4,
            "lg": spacing.SPACE_6,
            "xl": spacing.SPACE_8,
            "page": spacing.PAGE_PADDING,
        },
        "radius": {
            "sm": radius.RADIUS_SM,
            "md": radius.RADIUS_MD,
            "lg": radius.RADIUS_LG,
            "pill": radius.RADIUS_PILL,
        },
        "navigation": {
            "sidebar_bg": palette.DARK_SIDEBAR_BACKGROUND,
            "item": palette.DARK_SIDEBAR_ITEM,
            "item_hover": palette.DARK_SIDEBAR_ITEM_HOVER,
            "item_active": palette.DARK_SIDEBAR_ITEM_ACTIVE,
            "text": palette.DARK_SIDEBAR_TEXT,
            "text_active": palette.DARK_SIDEBAR_TEXT_ACTIVE,
            "muted": palette.DARK_SIDEBAR_MUTED,
            "border": palette.DARK_SIDEBAR_BORDER,
            "brand": palette.DARK_PRIMARY,
        },
        "input": {
            "background": palette.DARK_INPUT_BACKGROUND,
            "background_hover": palette.DARK_INPUT_BACKGROUND_HOVER,
            "border": palette.DARK_INPUT_BORDER,
            "border_hover": palette.DARK_INPUT_BORDER_HOVER,
            "border_focus": palette.DARK_INPUT_BORDER_FOCUS,
            "placeholder": palette.DARK_INPUT_PLACEHOLDER,
            "error": palette.DARK_DANGER,
            "disabled": palette.DARK_SURFACE_ALT,
        },
        "card": {
            "background": palette.DARK_CARD_BACKGROUND,
            "background_hover": palette.DARK_CARD_BACKGROUND_HOVER,
            "border": palette.DARK_CARD_BORDER,
            "shadow": palette.DARK_CARD_SHADOW,
        },
    },
    "inforhard_light": {
        "color": {
            "primary": palette.PRIMARY,
            "primary_hover": palette.PRIMARY_HOVER,
            "primary_soft": palette.PRIMARY_SOFT,
            "background": palette.LIGHT_BACKGROUND,
            "surface": palette.LIGHT_SURFACE,
            "surface_alt": palette.LIGHT_SURFACE_ALT,
            "border": palette.LIGHT_BORDER,
            "text": palette.LIGHT_TEXT,
            "muted": palette.LIGHT_MUTED,
            "success": palette.SUCCESS,
            "info": palette.INFO,
            "warning": palette.WARNING,
            "danger": palette.DANGER,
            "topbar_button": "#000000",
            "topbar": palette.LIGHT_TOPBAR,
        },
        "font": {
            "family": typography.FONT_FAMILY,
            "body": typography.FONT_SIZE_MD,
            "small": typography.FONT_SIZE_SM,
            "title": typography.FONT_SIZE_XL,
            "headline": typography.FONT_SIZE_2XL,
            "bold": typography.FONT_WEIGHT_BOLD,
        },
        "spacing": {
            "xs": spacing.SPACE_1,
            "sm": spacing.SPACE_2,
            "md": spacing.SPACE_4,
            "lg": spacing.SPACE_6,
            "xl": spacing.SPACE_8,
            "page": spacing.PAGE_PADDING,
        },
        "radius": {
            "sm": radius.RADIUS_SM,
            "md": radius.RADIUS_MD,
            "lg": radius.RADIUS_LG,
            "pill": radius.RADIUS_PILL,
        },
        "navigation": {
            "sidebar_bg": palette.LIGHT_SIDEBAR_BACKGROUND,
            "item": palette.LIGHT_SIDEBAR_ITEM,
            "item_hover": palette.LIGHT_SIDEBAR_ITEM_HOVER,
            "item_active": palette.LIGHT_SIDEBAR_ITEM_ACTIVE,
            "text": palette.LIGHT_SIDEBAR_TEXT,
            "text_active": palette.LIGHT_SIDEBAR_TEXT_ACTIVE,
            "muted": palette.LIGHT_SIDEBAR_MUTED,
            "border": palette.LIGHT_SIDEBAR_BORDER,
            "brand": palette.LIGHT_SIDEBAR_ITEM_ACTIVE,
        },
        "input": {
            "background": palette.LIGHT_INPUT_BACKGROUND,
            "background_hover": palette.LIGHT_INPUT_BACKGROUND_HOVER,
            "border": palette.LIGHT_INPUT_BORDER,
            "border_hover": palette.LIGHT_INPUT_BORDER_HOVER,
            "border_focus": palette.LIGHT_INPUT_BORDER_FOCUS,
            "placeholder": palette.LIGHT_INPUT_PLACEHOLDER,
            "error": palette.DANGER,
            "disabled": palette.LIGHT_SURFACE_ALT,
        },
        "card": {
            "background": palette.LIGHT_CARD_BACKGROUND,
            "background_hover": palette.LIGHT_CARD_BACKGROUND_HOVER,
            "border": palette.LIGHT_CARD_BORDER,
            "shadow": palette.LIGHT_CARD_SHADOW,
        },
    },
}


def get_tokens(theme_name: str = "inforhard_dark") -> dict:
    """Return a defensive copy of the selected theme token set."""

    return deepcopy(TOKENS.get(theme_name, TOKENS["inforhard_dark"]))
