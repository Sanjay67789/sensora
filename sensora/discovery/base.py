"""Abstract base class for all discovery scanners."""

from __future__ import annotations

from abc import ABC, abstractmethod

from sensora.core.result import Result


class BaseScanner(ABC):
    """Base class for all discovery scanners."""

    @abstractmethod
    def scan(self) -> Result:
        """
        Discover devices connected to a bus.

        Returns:
            Result containing discovered devices.
        """
        raise NotImplementedError
