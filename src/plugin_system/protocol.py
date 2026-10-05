"""Plugin protocol: Formatter contract."""

from typing import Protocol

from plugin_system.models import Record


class Formatter(Protocol):
    """
    Plugin contract for formatting a Record.

    Any object with `name` property and `format` method
    is structurally compatible with this protocol.
    """

    @property
    def name(self) -> str:
        """Unique identifier of the formatter."""
        ...

    def format(self, record: Record) -> str:
        """Format a Record into a string."""
        ...