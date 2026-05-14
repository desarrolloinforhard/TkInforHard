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
    },
}


def get_tokens(theme_name: str = "inforhard_dark") -> dict:
    """Return a defensive copy of the selected theme token set."""

    return deepcopy(TOKENS.get(theme_name, TOKENS["inforhard_dark"]))
