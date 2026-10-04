"""CLI entry point for README metadata updater."""

import argparse
import sys
from pathlib import Path

from .config import DEFAULT_README_PATH
from .core import update_readme


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for metadata updating.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Update build timestamp, app version, and patch version in README.md"
    )
    parser.add_argument(
        "app",
        type=str,
        help="Target app identifier (e.g. youtube, reddit, youtube-music, instagram, gboard, all)",
    )
    parser.add_argument(
        "--app-version",
        dest="app_version",
        type=str,
        default=None,
        help="Base application version (e.g. 21.16.256)",
    )
    parser.add_argument(
        "--patch-version",
        dest="patch_version",
        type=str,
        default=None,
        help="Patch bundle version or provider version (e.g. 1.45.0)",
    )
    parser.add_argument(
        "--timestamp",
        dest="timestamp",
        type=str,
        default=None,
        help="Custom timestamp string (e.g. '2026-10-04 07:45 UTC')",
    )
    parser.add_argument(
        "--readme",
        dest="readme",
        type=str,
        default=DEFAULT_README_PATH,
        help=f"Path to README file (default: {DEFAULT_README_PATH})",
    )

    return parser.parse_args()


def main() -> None:
    """Execute metadata updater command."""
    args = parse_args()
    readme_path = Path(args.readme)

    success = update_readme(
        app_id=args.app,
        readme_path=readme_path,
        app_version=args.app_version,
        patch_version=args.patch_version,
        custom_timestamp=args.timestamp,
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
