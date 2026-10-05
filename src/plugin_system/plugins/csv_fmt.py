"""CSV formatter plugin."""

from plugin_system.models import Record


class CsvFormatter:
    """Format a Record as a CSV line (structural plugin, no inheritance)."""

    @property
    def name(self) -> str:
        return "csv"

    def format(self, record: Record) -> str:
        return f"{record.name},{record.value}"