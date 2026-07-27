"""
Linux SPI bus implementation for Sensora.
"""

from __future__ import annotations

from sensora.buses.base import BaseBus
from sensora.buses.exceptions import (
    BusNotOpenError,
)


class LinuxSPIBus(BaseBus):
    """
    Native Linux SPI bus implementation.

    Parameters
    ----------
    bus
        Linux SPI bus number.

    device
        Chip select (CS) number.
    """

    def __init__(
        self,
        bus: int = 0,
        device: int = 0,
    ) -> None:
        self._bus = bus
        self._device = device
        self._spi = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        return f"SPI-{self._bus}.{self._device}"

    @property
    def bus_type(self) -> str:
        return "spi"

    @property
    def bus(self) -> int:
        return self._bus

    @property
    def device(self) -> int:
        return self._device

    @property
    def device_path(self) -> str:
        return f"/dev/spidev{self._bus}.{self._device}"

    @property
    def is_open(self) -> bool:
        return self._spi is not None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def open(self) -> None:
        """
        Open the SPI device.

        Actual Linux implementation will be added later.
        """
        raise NotImplementedError("Linux SPI backend is not implemented yet.")

    def close(self) -> None:
        """
        Close the SPI device.
        """
        self._spi = None

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def scan(self) -> list[int]:
        """
        SPI has no standard discovery mechanism.
        """
        return []

    def ping(
        self,
        address: int,
    ) -> bool:
        """
        SPI devices cannot be generically pinged.
        """
        return False

    # ------------------------------------------------------------------
    # Communication
    # ------------------------------------------------------------------

    def transfer(
        self,
        data: bytes,
    ) -> bytes:
        """
        Perform a full-duplex SPI transfer.
        """
        self._require_open()

        raise NotImplementedError("SPI transfer has not been implemented yet.")

    def write(
        self,
        data: bytes,
    ) -> None:
        """
        Write bytes to the SPI device.
        """
        self._require_open()

        raise NotImplementedError("SPI write has not been implemented yet.")

    def read(
        self,
        length: int,
    ) -> bytes:
        """
        Read bytes from the SPI device.
        """
        self._require_open()

        raise NotImplementedError("SPI read has not been implemented yet.")

    def configure(
        self,
        *,
        max_speed_hz: int,
        mode: int,
        bits_per_word: int = 8,
    ) -> None:
        """
        Configure SPI communication parameters.
        """
        self._require_open()

        raise NotImplementedError("SPI configuration has not been implemented yet.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _require_open(self) -> None:
        """
        Ensure the SPI device is open.
        """
        if not self.is_open:
            raise BusNotOpenError("SPI bus is not open.")
