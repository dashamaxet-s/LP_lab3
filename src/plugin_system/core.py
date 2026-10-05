"""Core dispatcher: works with plugins via the Formatter protocol."""

from plugin_system.models import Record
from plugin_system.protocol import Formatter


def format_record(formatter: Formatter, record: Record) -> str:
    """
    Format a Record using a single formatter (via protocol).

    The core does not know about concrete plugin classes.
    """
    return formatter.format(record)


def format_with_all(
    formatters: list[Formatter], record: Record
) -> dict[str, str]:
    """
    Format a Record with all given formatters.

    Returns a dict mapping formatter name to formatted string.
    """
    return {f.name: f.format(record) for f in formatters}