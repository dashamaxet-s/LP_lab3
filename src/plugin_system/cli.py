"""CLI entry point: assembly point for plugins."""

import argparse
import sys

from plugin_system.core import format_record
from plugin_system.models import Record
from plugin_system.plugins.csv_fmt import CsvFormatter
from plugin_system.plugins.json_fmt import JsonFormatter
from plugin_system.plugins.text_fmt import TextFormatter
from plugin_system.protocol import Formatter
from plugin_system.registry import Registry


def build_registry() -> Registry[Formatter]:
    """
    Build the plugin registry.

    This is the EXTERNAL assembly point.
    To add a new plugin, register it here. The core is NOT modified.
    """
    registry: Registry[Formatter] = Registry()
    registry.register("json", JsonFormatter())
    registry.register("csv", CsvFormatter())
    registry.register("text", TextFormatter())
    return registry


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Format a record using a plugin."
    )
    parser.add_argument(
        "--format",
        required=True,
        help="Plugin name (e.g. json, csv, text)",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Record name",
    )
    parser.add_argument(
        "--value",
        type=int,
        required=True,
        help="Record value (non-negative integer)",
    )

    args = parser.parse_args()

    try:
        record = Record(name=args.name, value=args.value)
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)

    registry = build_registry()
    formatter = registry.get(args.format)

    if formatter is None:
        available = ", ".join(registry.names())
        print(
            f"Unknown format: '{args.format}'. Available: {available}",
            file=sys.stderr,
        )
        sys.exit(1)

    result = format_record(formatter, record)
    print(result)


if __name__ == "__main__":
    main()