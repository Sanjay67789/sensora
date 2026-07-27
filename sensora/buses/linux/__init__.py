"""
Linux-specific bus implementations for Sensora.

This package contains the native Linux implementations used by the
platform-independent bus interfaces exposed by ``sensora.buses``.

Applications should normally import buses through the public API::

    from sensora.buses import I2CBus

rather than importing Linux implementations directly.

This separation allows Sensora to support multiple operating systems
and testing backends without changing the public interface.
"""

from .i2c import LinuxI2CBus
from .spi import LinuxSPIBus
from .uart import LinuxUARTBus

__all__ = (
    "LinuxI2CBus",
    "LinuxSPIBus",
    "LinuxUARTBus",
)
