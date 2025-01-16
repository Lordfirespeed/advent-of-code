from abc import abstractmethod
from typing import Protocol


__all__ = (
    "SupportsCopy",
)


class SupportsCopy(Protocol):
    """An ABC with one abstract method __copy__."""

    __slots__ = ()

    @abstractmethod
    def __copy__[T](self: T) -> T:
        pass
