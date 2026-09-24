#!/usr/bin/env python3
"""
README Timestamp Updater
Automatically updates the 'Last Updated' timestamp in README.md
for a given target app during GitHub Actions builds.
"""

import sys
import re
from datetime import datetime, timezone
from pathlib import Path


def get_current_utc_timestamp() -> str:
    """
    Generate a standardized UTC date and time string.

    Returns:
        Formatted timestamp string, e.g. '2026-09-22 05:45 UTC'.
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M UTC")


def update_readme_timestamp(app_id: str, readme_path: Path) -> bool:
    """
    Search and replace the timestamp comments for the target app in README.md.

    Args:
        app_id: Target app identifier (youtube, reddit, youtube-music, instagram, gboard, all).
        readme_path: Path to the README.md file.

    Returns:
        True if substitutions were made, False otherwise.
    """
    if not readme_path.exists():
        print(f"[-] Error: {readme_path} does not exist.")
        return False

    content = readme_path.read_text(encoding="utf-8")
    timestamp_str = get_current_utc_timestamp()
    changed = False

    targets = [app_id]
    if app_id == "all":
        targets = ["youtube", "reddit", "youtube-music", "youtube-music-whitelist", "instagram", "gboard"]
    elif app_id == "youtube-music":
        targets = ["youtube-music", "youtube-music-whitelist"]

    for target in targets:
        # Match pattern: `...` <!-- timestamp:target -->
        table_pattern = re.compile(rf"`[^`]+` <!-- timestamp:{re.escape(target)} -->")
        replacement_table = f"`{timestamp_str}` <!-- timestamp:{target} -->"

        if table_pattern.search(content):
            content = table_pattern.sub(replacement_table, content)
            changed = True

        # Match pattern: `...` <!-- section-timestamp:target -->
        section_pattern = re.compile(rf"`[^`]+` <!-- section-timestamp:{re.escape(target)} -->")
        replacement_section = f"`{timestamp_str}` <!-- section-timestamp:{target} -->"

        if section_pattern.search(content):
            content = section_pattern.sub(replacement_section, content)
            changed = True

    if changed:
        readme_path.write_text(content, encoding="utf-8")
        print(f"[+] Successfully updated timestamp for '{app_id}' to: {timestamp_str}")
        return True
    else:
        print(f"[-] No matching timestamp markers found for '{app_id}'.")
        return False


def main() -> None:
    """
    CLI entry point.
    Expects argument: <app_id> (e.g. youtube, reddit, youtube-music, instagram, gboard, all)
    """
    if len(sys.argv) < 2:
        print("Usage: python update_readme_timestamp.py <app_id> [path_to_readme]")
        sys.exit(1)

    app_id = sys.argv[1].lower()
    readme_path = Path("README.md")
    if len(sys.argv) >= 3:
        readme_path = Path(sys.argv[2])

    success = update_readme_timestamp(app_id, readme_path)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
