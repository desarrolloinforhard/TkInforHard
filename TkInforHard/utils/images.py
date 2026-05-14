"""Image utilities."""

from pathlib import Path


def asset_path(*parts: str) -> Path:
    """Return an absolute path inside the package assets directory."""

    return Path(__file__).resolve().parents[1] / "assets" / Path(*parts)

