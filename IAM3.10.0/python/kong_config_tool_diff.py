#!/usr/bin/env python3

import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import sys
import logging

logger = logging.getLogger("kong_config_tool")

def setup_logging(log_file=None):
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

    handlers = []

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

        # Redirect all stdout and stderr to the log file
        log_file_handle = open(log_file, "a")
        sys.stdout = log_file_handle
        sys.stderr = log_file_handle

    for handler in handlers:
        logger.addHandler(handler)

def find_latest_export_file(deck_dir):
    export_files = sorted(
        deck_dir.glob("kong-*.yaml"),
        key=os.path.getmtime,
        reverse=True
    )

    pattern = re.compile(r"kong-\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.yaml")
    for file in export_files:
        if pattern.fullmatch(file.name):
            return file
    return None

def export_kong_config():
    deck_dir = Path.cwd()
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = deck_dir / f"kong-{current_date}.yaml"

    # Trouver le dernier fichier d'export
    previous_export = find_latest_export_file(deck_dir)
    if previous_export:
        logger.info(f"Previous export found: {previous_export}")

    try:
        logger.info(f"Exporting Kong config to: {output_file}")
        result = subprocess.run(
            ["deck", "gateway", "dump", "-o", str(output_file)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        logger.debug(result.stdout)
        logger.debug(result.stderr)
        print(result.stdout)
        print(result.stderr)

        symlink_path = deck_dir / "kong.yaml"
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
        symlink_path.symlink_to(output_file.name)
        logger.info(f"Symlink created/updated: {symlink_path} -> {output_file.name}")

        # TODO: Générer un rapport de différences
        if previous_export:
            diff_file = deck_dir / f"diff-{previous_export.stem}-vs-{output_file.stem}.txt"
            subprocess.run(
                ["diff", "-u", str(previous_export), str(output_file)],
                stdout=diff_file.open("w"),
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"Diff report generated: {diff_file}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Export failed: {e}")
        logger.error(e.stderr)
        print(e.stderr)
        sys.exit(1)

def import_kong_config():
    deck_file = Path.cwd() / "kong.yaml"
    if not deck_file.exists():
        logger.error(f"Configuration file {deck_file} not found.")
        sys.exit(1)

    try:
        logger.info("Syncing kong.yaml to gateway...")
        result = subprocess.run(
            ["deck", "gateway", "sync", str(deck_file)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Log and print deck output
        logger.debug(result.stdout)
        logger.debug(result.stderr)
        # print(result.stdout)
        # print(result.stderr)

        logger.info("Sync completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Sync failed: {e}")
        logger.error(e.stderr)
        print(e.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Tool to export or import Kong Gateway configuration using deck.\n\n"
            "Exactly one of the options --export or --import is required.\n\n"
            "Examples:\n"
            "  python kong_config_tool.py --export --log export.log\n"
            "  python kong_config_tool.py --import --log import.log\n\n"
            "For help, run:\n"
            "  python kong_config_tool.py --help"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--export", dest="export_config", action="store_true",
                       help="Export Kong configuration to a timestamped YAML file and create/update kong.yaml symlink.")
    group.add_argument("-i", "--import", dest="import_config", action="store_true",
                       help="Import (sync) Kong configuration from kong.yaml into Kong Gateway.")
    
    parser.add_argument(
        "--log",
        dest="log_file",
        nargs="?",
        const="kong_config_tool.log",
        help="Enable logging to a file. Use default 'kong_config_tool.log' if no path is given."
    )

    args = parser.parse_args()

    setup_logging(args.log_file)

    if args.export_config:
        export_kong_config()
    elif args.import_config:
        import_kong_config()

if __name__ == "__main__":
    main()
