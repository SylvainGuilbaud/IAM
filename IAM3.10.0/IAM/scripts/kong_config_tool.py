#!/usr/bin/env python3

import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import sys

def export_kong_config():
    deck_dir = Path.cwd()
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = deck_dir / f"kong-{current_date}.yaml"

    try:
        print(f"[INFO] Exporting Kong config to: {output_file}")
        subprocess.run(["deck", "gateway", "dump", "-o", str(output_file)], check=True)

        symlink_path = deck_dir / "kong.yaml"
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
        symlink_path.symlink_to(output_file.name)
        print(f"[INFO] Symlink created/updated: {symlink_path} -> {output_file.name}")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Export failed: {e}")
        sys.exit(1)

def import_kong_config():
    deck_file = Path.cwd() / "kong.yaml"
    if not deck_file.exists():
        print(f"[ERROR] Configuration file {deck_file} not found.")
        sys.exit(1)

    try:
        print(f"[INFO] Syncing kong.yaml to gateway...")
        subprocess.run(["deck", "gateway", "sync", str(deck_file)], check=True)
        print("[INFO] Sync completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Sync failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Tool to export or import Kong Gateway configuration using deck.\n\n"
            "Exactly one of the options --export or --import is required.\n\n"
            "Examples:\n"
            "  python kong_config_tool.py --export   # Export Kong config to kong-<date>.yaml and update kong.yaml\n"
            "  python kong_config_tool.py --import   # Import config from kong.yaml into Kong Gateway\n\n"
            "For help, run:\n"
            "  python kong_config_tool.py --help"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-e", "--export",
        dest="export_config", 
        action="store_true",
        help="Export Kong configuration to a timestamped YAML file and create/update kong.yaml symlink."
    )
    group.add_argument(
        "-i", "--import",
        dest="import_config",  # ✅ nom interne autorisé
        action="store_true",
        help="Import (sync) Kong configuration from kong.yaml into Kong Gateway."
    )

    args = parser.parse_args()

    if args.export_config:
        export_kong_config()
    elif args.import_config:
        import_kong_config()

if __name__ == "__main__":
    main()
