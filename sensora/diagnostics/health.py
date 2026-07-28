"""
Sensora hardware health diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from sensora.database.exceptions import SchemaValidationError
from sensora.database.loader import DatabaseLoader


@dataclass
class HealthCheck:
    """
    Single diagnostic result.
    """

    name: str
    status: str
    message: str
    causes: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


class HealthDiagnostics:
    """
    Run Sensora diagnostic checks.
    """

    def __init__(self) -> None:
        self.results: list[HealthCheck] = []

    def run(self) -> list[HealthCheck]:
        """
        Execute all health checks.
        """

        self.results.clear()

        self.check_database()
        self.check_i2c()
        self.check_spi()
        self.check_uart()
        self.check_onewire()

        return self.results

    def add(
        self,
        name: str,
        status: str,
        message: str,
        causes: list[str] | None = None,
        suggestions: list[str] | None = None,
    ) -> None:
        """
        Add diagnostic result.
        """

        self.results.append(
            HealthCheck(
                name=name,
                status=status,
                message=message,
                causes=causes or [],
                suggestions=suggestions or [],
            )
        )

    def check_database(self) -> None:
        """
        Check Sensora database.
        """

        try:
            registry = DatabaseLoader().load()

            self.add(
                name="Database",
                status="PASS",
                message=(
                    f"{registry.vendor_count} vendors, "
                    f"{registry.device_count} devices loaded"
                ),
            )

        except SchemaValidationError:
            self.add(
                name="Database",
                status="FAIL",
                message="Database validation failed.",
                causes=[
                    "Invalid YAML definition",
                    "Schema mismatch",
                ],
                suggestions=[
                    "Check definitions/*.yaml",
                    "Run schema validation",
                ],
            )

    def check_i2c(self) -> None:
        """
        Check I2C availability.
        """

        devices = list(Path("/dev").glob("i2c-*"))

        if devices:
            self.add(
                name="I2C",
                status="PASS",
                message=f"{len(devices)} Linux adapters available",
            )

        else:
            self.add(
                name="I2C",
                status="WARN",
                message="No I2C adapter detected.",
                causes=[
                    "I2C kernel module disabled",
                    "Hardware does not expose I2C",
                ],
                suggestions=[
                    "Check i2c kernel modules",
                    "Run: ls /dev/i2c-*",
                ],
            )

    def check_spi(self) -> None:
        """
        Check SPI availability.
        """

        devices = list(Path("/dev").glob("spidev*"))

        if devices:
            self.add(
                name="SPI",
                status="PASS",
                message=f"{len(devices)} SPI device(s) available",
            )

        else:
            self.add(
                name="SPI",
                status="WARN",
                message="No SPI controller detected.",
                causes=[
                    "SPI disabled in kernel",
                    "No SPI hardware connected",
                ],
                suggestions=[
                    "Check: ls /dev/spidev*",
                ],
            )

    def check_uart(self) -> None:
        """
        Check external UART devices.
        """

        devices = list(Path("/dev").glob("ttyUSB*")) + list(
            Path("/dev").glob("ttyACM*")
        )

        if devices:
            self.add(
                name="UART",
                status="PASS",
                message=f"{len(devices)} external UART device(s)",
            )

        else:
            self.add(
                name="UART",
                status="WARN",
                message="No external UART devices detected.",
                causes=[
                    "USB serial adapter not connected",
                    "Driver missing",
                ],
                suggestions=[
                    "Connect USB-UART adapter",
                    "Check: ls /dev/ttyUSB*",
                ],
            )

    def check_onewire(self) -> None:
        """
        Check 1-Wire sensors.
        """

        path = Path("/sys/bus/w1/devices")

        sensors = []

        if path.exists():
            sensors = [item for item in path.iterdir() if item.name.startswith("28-")]

        if sensors:
            self.add(
                name="1-Wire",
                status="PASS",
                message=f"{len(sensors)} sensor(s) detected",
            )

        else:
            self.add(
                name="1-Wire",
                status="WARN",
                message="No 1-Wire sensors detected.",
                causes=[
                    "DS18B20 not connected",
                    "w1 kernel modules missing",
                    "Incorrect GPIO configuration",
                ],
                suggestions=[
                    "Check: lsmod | grep w1",
                    "Check pull-up resistor",
                ],
            )
