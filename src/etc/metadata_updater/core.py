"""Core logic for updating markdown markers in README.md."""

import re
from pathlib import Path
from typing import Optional

from .config import TARGET_MAPPINGS
from .utils import (
    format_patch_version,
    get_current_utc_timestamp,
    normalize_version,
    read_text_safe,
    write_text_safe,
)


def update_target_markers(
    content: str,
    target: str,
    timestamp: str,
    app_version: Optional[str] = None,
    patch_version: Optional[str] = None,
) -> tuple[str, bool]:
    """Update all markers for a specific target in the markdown content.

    Args:
        content: Markdown content string.
        target: Target identifier (e.g. 'youtube', 'gboard').
        timestamp: Standardized timestamp string.
        app_version: Optional base app version string.
        patch_version: Optional patch version string.

    Returns:
        Tuple of (updated_content, was_modified).
    """
    modified = False
    escaped_target = re.escape(target)

    # 1. Update Table timestamp: `...` <!-- timestamp:<target> -->
    table_ts_pat = re.compile(rf"`[^`]*` <!-- timestamp:{escaped_target} -->")
    replacement_table_ts = f"`{timestamp}` <!-- timestamp:{target} -->"
    if table_ts_pat.search(content):
        content = table_ts_pat.sub(replacement_table_ts, content)
        modified = True

    # 2. Update Section timestamp: `...` <!-- section-timestamp:<target> -->
    section_ts_pat = re.compile(rf"`[^`]*` <!-- section-timestamp:{escaped_target} -->")
    replacement_section_ts = f"`{timestamp}` <!-- section-timestamp:{target} -->"
    if section_ts_pat.search(content):
        content = section_ts_pat.sub(replacement_section_ts, content)
        modified = True

    # 3. Update Base App Version if provided
    if app_version:
        norm_app_ver = normalize_version(app_version)

        # Table app-version: `...` <!-- app-version:<target> -->
        table_app_pat = re.compile(rf"`[^`]*` <!-- app-version:{escaped_target} -->")
        replacement_table_app = f"`{norm_app_ver}` <!-- app-version:{target} -->"
        if table_app_pat.search(content):
            content = table_app_pat.sub(replacement_table_app, content)
            modified = True

        # Section app-version: `...` <!-- section-app-version:<target> -->
        section_app_pat = re.compile(rf"`[^`]*` <!-- section-app-version:{escaped_target} -->")
        replacement_section_app = f"`{norm_app_ver}` <!-- section-app-version:{target} -->"
        if section_app_pat.search(content):
            content = section_app_pat.sub(replacement_section_app, content)
            modified = True

    # 4. Update Patch Version if provided
    if patch_version:
        formatted_patch = format_patch_version(target, patch_version)

        # Table patch-version: `...` <!-- patch-version:<target> -->
        table_patch_pat = re.compile(rf"`[^`]*` <!-- patch-version:{escaped_target} -->")
        replacement_table_patch = f"`{formatted_patch}` <!-- patch-version:{target} -->"
        if table_patch_pat.search(content):
            content = table_patch_pat.sub(replacement_table_patch, content)
            modified = True

        # Section patch-version: `...` <!-- section-patch-version:<target> -->
        section_patch_pat = re.compile(rf"`[^`]*` <!-- section-patch-version:{escaped_target} -->")
        replacement_section_patch = f"`{formatted_patch}` <!-- section-patch-version:{target} -->"
        if section_patch_pat.search(content):
            content = section_patch_pat.sub(replacement_section_patch, content)
            modified = True

    return content, modified


def update_readme(
    app_id: str,
    readme_path: Path,
    app_version: Optional[str] = None,
    patch_version: Optional[str] = None,
    custom_timestamp: Optional[str] = None,
) -> bool:
    """Perform full metadata update on the README file.

    Args:
        app_id: Application identifier (e.g. 'youtube', 'all').
        readme_path: Path object pointing to README.md.
        app_version: Optional base app version string.
        patch_version: Optional patch version string.
        custom_timestamp: Optional pre-defined timestamp string.

    Returns:
        True if changes were made and saved, False otherwise.
    """
    content = read_text_safe(readme_path)
    if content is None:
        print(f"[-] Error: {readme_path} does not exist.")
        return False

    targets = TARGET_MAPPINGS.get(app_id.lower(), [app_id.lower()])
    timestamp = custom_timestamp or get_current_utc_timestamp()
    overall_modified = False

    for target in targets:
        content, mod = update_target_markers(
            content=content,
            target=target,
            timestamp=timestamp,
            app_version=app_version,
            patch_version=patch_version,
        )
        if mod:
            overall_modified = True

    if overall_modified:
        write_text_safe(readme_path, content)
        ver_info = []
        if app_version:
            ver_info.append(f"app={normalize_version(app_version)}")
        if patch_version:
            ver_info.append(f"patch={format_patch_version(app_id, patch_version)}")
        ver_msg = f" ({', '.join(ver_info)})" if ver_info else ""
        print(f"[+] Successfully updated metadata for '{app_id}' to: {timestamp}{ver_msg}")
        return True

    print(f"[-] No matching markers modified for '{app_id}'.")
    return False
