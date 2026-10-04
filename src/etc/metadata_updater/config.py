"""Configuration settings and target mappings for metadata updater."""

from typing import Dict, List

# Target mappings: Maps primary app_id to all relevant comment markers
TARGET_MAPPINGS: Dict[str, List[str]] = {
    "youtube": ["youtube"],
    "youtube-music": ["youtube-music", "youtube-music-whitelist"],
    "reddit": ["reddit"],
    "instagram": ["instagram"],
    "gboard": ["gboard"],
    "all": ["youtube", "youtube-music", "youtube-music-whitelist", "instagram", "reddit", "gboard"],
}

# Display names for patch providers
PATCH_PROVIDERS: Dict[str, str] = {
    "youtube": "Morphe",
    "youtube-music": "Morphe",
    "youtube-music-whitelist": "Morphe",
    "reddit": "Morphe",
    "instagram": "Piko",
    "gboard": "Gboard Patches",
}

# Default README path relative to repo root
DEFAULT_README_PATH: str = "README.md"
