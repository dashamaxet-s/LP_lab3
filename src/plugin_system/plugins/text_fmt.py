"""Plain text formatter plugin."""

from plugin_system.models import Record


class TextFormatter:
    """Format a Record as plain text (structural plugin, no inheritance)."""

    @property
    def name(self) -> str:
        return "text"

    def format(self, record: Record) -> str:
        return f"{record.name} = {record.value}"