"""
Abstract GPIO communication bus interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sensora.buses.base import BaseBus


class GPIOBus(BaseBus, ABC):
    """
    Abstract base class for GPIO communication buses.

    Platform-specific GPIO backends should inherit from this class.
    """

    __slots__ = ()

    @abstractmethod
    def read(self, offset: int) -> bool:
        """
        Read the logic level of a GPIO line.

        Parameters
        ----------
        offset
            GPIO line offset.

        Returns
        -------
        bool
            True if the line is high, otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    def write(
        self,
        offset: int,
        value: bool,
    ) -> None:
        """
        Set the logic level of a GPIO line.

        Parameters
        ----------
        offset
            GPIO line offset.

        value
            Output logic level.
        """
        raise NotImplementedError
