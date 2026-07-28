"""
Info command for Sensora.
"""

from __future__ import annotations

import platform
import sys
from pathlib import Path

import typer

from sensora.database.exceptions import SchemaValidationError
from sensora.database.loader import DatabaseLoader

app = typer.Typer(
    help="Show Sensora system information.",
)


def count_devices(pattern: str) -> list[Path]:
    """
    Count Linux device nodes.
    """
    return sorted(Path("/dev").glob(pattern))


@app.callback(invoke_without_command=True)
def main() -> None:
    """
    Display Sensora system information.
    """

    typer.echo()

    typer.secho(
        "Sensora System Information",
        fg=typer.colors.CYAN,
        bold=True,
    )

    typer.echo()

    typer.echo(f"Platform      : {platform.system()}")

    typer.echo(f"Kernel        : {platform.release()}")

    typer.echo(f"Architecture  : {platform.machine()}")

    typer.echo(f"Python        : {sys.version.split()[0]}")

    typer.echo()

    typer.secho(
        "External Hardware Interfaces",
        fg=typer.colors.GREEN,
        bold=True,
    )

    typer.echo()

    # ---------------- I2C ----------------

    i2c_adapters = count_devices("i2c-*")

    typer.echo("I2C")

    typer.echo(f"    Kernel adapters : {len(i2c_adapters)}")

    typer.echo(f"    Status          : {'Available' if i2c_adapters else 'Not found'}")

    typer.echo("    Detection       : Use 'sensora scan --bus i2c'")

    typer.echo()

    # ---------------- SPI ----------------

    spi_devices = count_devices("spidev*")

    typer.echo("SPI")

    typer.echo(f"    Controllers     : {len(spi_devices)}")

    typer.echo(f"    Status          : {'Available' if spi_devices else 'Not found'}")

    typer.echo()

    # ---------------- UART ----------------

    external_uart = count_devices("ttyUSB*") + count_devices("ttyACM*")

    internal_uart = count_devices("ttyS*")

    typer.echo("UART")

    typer.echo(f"    External ports  : {len(external_uart)}")

    typer.echo(f"    Kernel ports    : {len(internal_uart)}")

    typer.echo(f"    Status          : {'Available' if external_uart else 'Not found'}")

    typer.echo()

    # ---------------- 1-Wire ----------------

    onewire_path = Path("/sys/bus/w1/devices")

    onewire_devices: list[Path] = []

    if onewire_path.exists():
        onewire_devices = [
            device for device in onewire_path.iterdir() if device.name.startswith("28-")
        ]

    typer.echo("1-Wire")

    typer.echo(f"    Sensors         : {len(onewire_devices)}")

    typer.echo(
        f"    Status          : {'Available' if onewire_devices else 'Not found'}"
    )

    typer.echo()

    # ---------------- Database ----------------

    typer.secho(
        "Database",
        fg=typer.colors.YELLOW,
        bold=True,
    )

    typer.echo()

    try:
        registry = DatabaseLoader().load()

        typer.echo(f"Vendors       : {registry.vendor_count}")

        typer.echo(f"Devices       : {registry.device_count}")

        typer.echo("Status        : Loaded")

    except SchemaValidationError as exc:
        typer.echo("Status        : Failed")

        typer.secho(
            f"Error         : {exc}",
            fg=typer.colors.RED,
        )
