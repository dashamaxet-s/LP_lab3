"""Generic Registry[T] for storing plugins by key."""

from typing import Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """
    Generic registry for storing items of type T by name.

    Preserves the concrete type T (not Any) through mypy.
    """

    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def register(self, name: str, item: T) -> None:
        """Register an item under the given name."""
        if not name:
            raise ValueError("name must not be empty")
        self._items[name] = item

    def get(self, name: str) -> T | None:
        """Return item by name, or None if not found."""
        return self._items.get(name)

    def all_items(self) -> list[T]:
        """Return all registered items."""
        return list(self._items.values())

    def names(self) -> list[str]:
        """Return all registered names."""
        return list(self._items.keys())