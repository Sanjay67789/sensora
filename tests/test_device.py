"""Tests for the Device model."""

from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus


def test_device():
    sensor = Device(
        name="BME280",
        manufacturer="Bosch",
        bus=BusType.I2C,
        address=0x76,
        chip_id=0x60,
        status=DeviceStatus.DETECTED,
        description="Environmental sensor",
    )

    print(sensor)


if __name__ == "__main__":
    test_device()
