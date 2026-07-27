"""
Linux 1-Wire bus backend.
"""

from __future__ import annotations

from pathlib import Path
from types import TracebackType
from typing import Self

from sensora.buses.exceptions import (
    BusError,
    DeviceCommunicationError,
)
from sensora.buses.linux.base import LinuxBus
from sensora.buses.onewire import OneWireBus


class LinuxOneWireBus(LinuxBus, OneWireBus):
    """
    Native Linux implementation of the 1-Wire bus.

    This backend communicates through the Linux ``w1`` sysfs
    interface located under ``/sys/bus/w1/devices``.
    """

    __slots__ = ("_root",)

    DEFAULT_ROOT = Path("/sys/bus/w1/devices")

    def __init__(
        self,
        root: Path | str | None = None,
    ) -> None:
        """
        Initialize the Linux 1-Wire backend.

        Parameters
        ----------
        root
            Optional sysfs root directory.
        """
        self._root = Path(root) if root is not None else self.DEFAULT_ROOT

    @property
    def name(self) -> str:
        """Return backend name."""
        return "Linux 1-Wire"

    @property
    def bus_type(self) -> str:
        """Return bus type."""
        return "onewire"

    @property
    def is_open(self) -> bool:
        """Return whether the bus is available."""
        return self._root.exists()

    def open(self) -> None:
        """
        Verify the Linux 1-Wire subsystem exists.
        """
        if not self._root.exists():
            raise BusError(f"1-Wire sysfs not found: {self._root}")

    def close(self) -> None:
        """
        Close the backend.

        Linux sysfs requires no cleanup.
        """
        return

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def scan(self) -> list[str]:
        """
        Discover connected 1-Wire devices.

        Returns
        -------
        list[str]
            ROM identifiers of discovered devices.
        """
        self.open()

        devices: list[str] = []

        try:
            for entry in self._root.iterdir():
                if not entry.is_dir():
                    continue

                if entry.name.startswith("."):
                    continue

                if entry.name.startswith("w1_bus_master"):
                    continue

                devices.append(entry.name)

        except OSError as exc:
            raise BusError("Failed to enumerate 1-Wire devices.") from exc

        return sorted(devices)

    def exists(
        self,
        rom: str,
    ) -> bool:
        """
        Determine whether a device exists.

        Parameters
        ----------
        rom
            Device ROM identifier.

        Returns
        -------
        bool
            True if the device exists.
        """
        self.open()
        return self.device_path(rom).exists()

    def device_path(
        self,
        rom: str,
    ) -> Path:
        """
        Return the filesystem path of a device.

        Parameters
        ----------
        rom
            Device ROM identifier.

        Returns
        -------
        Path
            Device directory.
        """
        if not rom:
            raise ValueError("ROM identifier cannot be empty.")

        if "/" in rom:
            raise ValueError(f"Invalid ROM identifier: {rom!r}")

        return self._root / rom

    def read_text(
        self,
        rom: str,
        filename: str,
    ) -> str:
        """
        Read a text file from a 1-Wire device.
        """
        path = self.device_path(rom) / filename

        try:
            return path.read_text(encoding="utf-8")

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to read '{filename}' from '{rom}'."
            ) from exc

    def read_bytes(
        self,
        rom: str,
        filename: str,
    ) -> bytes:
        """
        Read a binary file from a 1-Wire device.
        """
        path = self.device_path(rom) / filename

        try:
            return path.read_bytes()

        except OSError as exc:
            raise DeviceCommunicationError(
                f"Failed to read '{filename}' from '{rom}'."
            ) from exc
