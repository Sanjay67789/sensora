"""
Abstract GPIO communication bus interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sensora.buses.base import BaseBus


class GPIOBus(BaseBus, ABC):
    """
    Abstract base class for GPIO communication buses.
    """

    __slots__ = ()

    @abstractmethod
    def read(
        self,
        offset: int,
    ) -> bool:
        """
        Read a GPIO line.

        Parameters
        ----------
        offset
            GPIO line offset.

        Returns
        -------
        bool
            Logic level of the GPIO line.
        """
        raise NotImplementedError

    @abstractmethod
    def write(
        self,
        offset: int,
        value: bool,
    ) -> None:
        """
        Write a GPIO line.

        Parameters
        ----------
        offset
            GPIO line offset.

        value
            Logic level to write.
        """
        raise NotImplementedError
