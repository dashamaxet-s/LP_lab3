"""Data model: Record dataclass with validation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Record:
    """
    A single record to be formatted.

    Validation rules:
    - name must not be empty
    - value must be non-negative
    """

    name: str
    value: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if self.value < 0:
            raise ValueError("value must be non-negative")