"""Tests for the plugin system."""

import pytest

from plugin_system.core import format_record, format_with_all
from plugin_system.models import Record
from plugin_system.plugins.csv_fmt import CsvFormatter
from plugin_system.plugins.json_fmt import JsonFormatter
from plugin_system.plugins.text_fmt import TextFormatter
from plugin_system.registry import Registry


# ---------- Positive tests: each plugin gives expected result ----------


def test_json_formatter() -> None:
    """JsonFormatter produces valid JSON output."""
    record = Record(name="Alice", value=42)
    result = JsonFormatter().format(record)
    assert result == '{"name": "Alice", "value": 42}'


def test_csv_formatter() -> None:
    """CsvFormatter produces a CSV line."""
    record = Record(name="Alice", value=42)
    result = CsvFormatter().format(record)
    assert result == "Alice,42"


def test_text_formatter() -> None:
    """TextFormatter produces a plain text line."""
    record = Record(name="Alice", value=42)
    result = TextFormatter().format(record)
    assert result == "Alice = 42"


# ---------- Positive tests: Record and Registry ----------


def test_record_valid() -> None:
    """Record can be created with valid data."""
    record = Record(name="Bob", value=0)
    assert record.name == "Bob"
    assert record.value == 0


def test_registry_register_and_get() -> None:
    """Registry stores and returns items by name."""
    registry: Registry[str] = Registry()
    registry.register("a", "hello")
    assert registry.get("a") == "hello"
    assert registry.get("missing") is None
    assert registry.names() == ["a"]


# ---------- Negative tests: validation raises ValueError ----------


def test_record_empty_name_raises() -> None:
    """Empty name raises ValueError."""
    with pytest.raises(ValueError, match="name must not be empty"):
        Record(name="", value=42)


def test_record_negative_value_raises() -> None:
    """Negative value raises ValueError."""
    with pytest.raises(ValueError, match="value must be non-negative"):
        Record(name="Alice", value=-1)


def test_registry_empty_name_raises() -> None:
    """Registry.register raises ValueError for empty name."""
    registry: Registry[str] = Registry()
    with pytest.raises(ValueError, match="name must not be empty"):
        registry.register("", "value")


# ---------- Core tests ----------


def test_core_format_record() -> None:
    """Core dispatcher formats a record via protocol."""
    record = Record(name="Alice", value=42)
    result = format_record(JsonFormatter(), record)
    assert result == '{"name": "Alice", "value": 42}'


def test_core_format_with_all() -> None:
    """Core dispatcher formats a record with all formatters."""
    record = Record(name="Alice", value=42)
    result = format_with_all(
        [JsonFormatter(), CsvFormatter(), TextFormatter()], record
    )
    assert result == {
        "json": '{"name": "Alice", "value": 42}',
        "csv": "Alice,42",
        "text": "Alice = 42",
    }


# ---------- KEY TEST: new plugin without modifying the core ----------


class UpperFormatter:
    """
    A brand-new plugin defined INSIDE the test.

    It is not imported from the package, the core does not know about it.
    It only matches the Formatter protocol structurally.
    """

    @property
    def name(self) -> str:
        return "upper"

    def format(self, record: Record) -> str:
        return f"{record.name.upper()}={record.value}"


def test_new_plugin_without_core_change() -> None:
    """
    A new plugin can be registered and used by the core
    WITHOUT any modification to the core source code.
    """
    registry: Registry[object] = Registry()
    registry.register("upper", UpperFormatter())

    plugin = registry.get("upper")
    assert plugin is not None

    record = Record(name="Alice", value=42)
    result = format_record(plugin, record)   # type: ignore[arg-type]
    assert result == "ALICE=42"