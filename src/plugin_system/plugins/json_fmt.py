"""JSON formatter plugin."""

import json

from plugin_system.models import Record


class JsonFormatter:
    """Format a Record as JSON (structural plugin, no inheritance)."""

    @property
    def name(self) -> str:
        return "json"

    def format(self, record: Record) -> str:
        return json.dumps({"name": record.name, "value": record.value})