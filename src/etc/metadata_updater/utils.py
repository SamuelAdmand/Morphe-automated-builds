"""Utility helpers for date formatting, version normalization, and file I/O."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import PATCH_PROVIDERS


def get_current_utc_timestamp() -> str:
    """Generate a standardized UTC date and time string.

    Returns:
        Formatted timestamp string, e.g. '2026-10-04 07:45 UTC'.
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M UTC")


def normalize_version(version_str: Optional[str]) -> str:
    """Ensure version string is prefixed with 'v' for standard presentation.

    Args:
        version_str: Raw version string (e.g. '21.16.256' or 'v21.16.256').

    Returns:
        Standardized version string starting with 'v', or empty string if None.
    """
    if not version_str:
        return ""
    cleaned = version_str.strip()
    if cleaned and not cleaned.lower().startswith("v"):
        return f"v{cleaned}"
    return cleaned


def format_patch_version(target: str, raw_patch_ver: Optional[str]) -> str:
    """Format patch version with the provider name (e.g. 'Morphe v1.45.0').

    Args:
        target: Target app key (e.g. 'youtube', 'instagram', 'gboard').
        raw_patch_ver: Raw patch version string (e.g. '1.45.0', 'v1.45.0', 'patches-1.45.0.mpp').

    Returns:
        Formatted patch version label, e.g. 'Morphe v1.45.0'.
    """
    if not raw_patch_ver:
        return ""

    provider = PATCH_PROVIDERS.get(target, "Morphe")
    ver = raw_patch_ver.strip()

    # Strip unwanted prefix/suffix if a filename was passed
    if ver.endswith(".mpp"):
        ver = ver[:-4]
    if ver.startswith("patches-"):
        ver = ver[len("patches-"):]
    elif ver.startswith("piko-"):
        ver = ver[len("piko-"):]
    elif ver.startswith("Gboard-patches-"):
        ver = ver[len("Gboard-patches-"):]

    norm_ver = normalize_version(ver)

    # Avoid duplicate provider names if already included
    if norm_ver.lower().startswith(provider.lower()):
        return norm_ver
    return f"{provider} {norm_ver}"


def read_text_safe(path: Path) -> Optional[str]:
    """Read file content with UTF-8 encoding safely.

    Args:
        path: Path to the file.

    Returns:
        File content string, or None if file does not exist.
    """
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def write_text_safe(path: Path, content: str) -> None:
    """Write text content to file safely with UTF-8 encoding.

    Args:
        path: Path to the target file.
        content: String content to write.
    """
    path.write_text(content, encoding="utf-8")
