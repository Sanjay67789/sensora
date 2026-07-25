"""Tests for the Result model."""

from sensora.core.device import Device
from sensora.core.enums import BusType, DeviceStatus
from sensora.core.result import Result


def test_result():
    device = Device(
        name="BME280",
        manufacturer="Bosch",
        bus=BusType.I2C,
        address=0x76,
        chip_id=0x60,
        status=DeviceStatus.DETECTED,
    )

    result = Result(
        success=True,
        message="1 device discovered",
        devices=[device],
    )

    print(result)


if __name__ == "__main__":
    test_result()
