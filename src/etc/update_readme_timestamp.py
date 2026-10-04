#!/usr/bin/env python3
"""README Metadata & Timestamp Updater.

Backwards-compatible wrapper that updates timestamp, app version, and
patch version in README.md using the modular metadata_updater package.
"""

import sys
from pathlib import Path

# Add current directory to path if needed for relative imports
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from metadata_updater.core import update_readme
from metadata_updater.main import main as cli_main


def main() -> None:
    """CLI entry point supporting both legacy positional and modern flags."""
    # If using modern flag syntax or help, forward to cli_main
    if any(arg.startswith("-") for arg in sys.argv[1:]):
        cli_main()
        return

    if len(sys.argv) < 2:
        print("Usage: python update_readme_timestamp.py <app_id> [path_to_readme]")
        print("       python update_readme_timestamp.py <app_id> --app-version <ver> --patch-version <patch>")
        sys.exit(1)

    app_id = sys.argv[1].lower()
    readme_path = Path("README.md")
    if len(sys.argv) >= 3:
        readme_path = Path(sys.argv[2])

    success = update_readme(app_id=app_id, readme_path=readme_path)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
