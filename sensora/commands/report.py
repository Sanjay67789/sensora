"""
Report command for Sensora.
"""

from __future__ import annotations

import platform
import sys
from datetime import UTC, datetime

import typer

from sensora.buses.linux.onewire import LinuxOneWireBus
from sensora.database.exceptions import SchemaValidationError
from sensora.database.loader import DatabaseLoader
from sensora.database.matcher import DeviceMatcher
from sensora.discovery.i2c import I2CScanner
from sensora.discovery.onewire import OneWireScanner
from sensora.discovery.scanner import Scanner
from sensora.discovery.spi import SPIScanner
from sensora.discovery.uart import UARTScanner

app = typer.Typer(
    help="Generate Sensora hardware report.",
)


@app.callback(invoke_without_command=True)
def main(
    quick: bool = typer.Option(
        False,
        "--quick",
        help="Generate report without hardware scanning.",
    ),
    full: bool = typer.Option(
        False,
        "--full",
        help="Perform complete hardware scan.",
    ),
) -> None:
    """
    Generate complete hardware diagnostic report.
    """

    typer.echo()

    typer.secho(
        "=================================",
        fg=typer.colors.CYAN,
    )

    typer.secho(
        "        Sensora Report",
        fg=typer.colors.CYAN,
        bold=True,
    )

    typer.secho(
        "=================================",
        fg=typer.colors.CYAN,
    )

    typer.echo()

    # System

    typer.secho(
        "System",
        fg=typer.colors.GREEN,
        bold=True,
    )

    typer.echo(f"OS           : {platform.system()}")

    typer.echo(f"Kernel       : {platform.release()}")

    typer.echo(f"Architecture : {platform.machine()}")

    typer.echo(f"Python       : {sys.version.split()[0]}")

    typer.echo()

    # Database

    typer.secho(
        "Database",
        fg=typer.colors.GREEN,
        bold=True,
    )

    try:

        registry = DatabaseLoader().load()

        typer.echo(f"Vendors      : {registry.vendor_count}")

        typer.echo(f"Devices      : {registry.device_count}")

        typer.echo("Status       : Loaded")

    except SchemaValidationError as exc:

        typer.secho(
            "Status       : Failed",
            fg=typer.colors.RED,
        )

        typer.echo(f"Error        : {exc}")

        registry = None

    typer.echo()

    # Hardware

    typer.secho(
        "Detected Hardware",
        fg=typer.colors.GREEN,
        bold=True,
    )

    typer.echo()

    result = None

    if quick:

        typer.echo("Hardware scan skipped (quick mode).")

    else:

        scanner = Scanner()

        if registry:

            matcher = DeviceMatcher(registry)

            scanner.register(I2CScanner(matcher=matcher))

        scanner.register(SPIScanner())

        scanner.register(UARTScanner())

        scanner.register(OneWireScanner(LinuxOneWireBus()))

        result = scanner.scan()

        if not result.devices:

            typer.echo("No supported devices detected.")

        else:

            for index, device in enumerate(
                result.devices,
                start=1,
            ):

                typer.secho(
                    f"[{index}] {device.name}",
                    fg=typer.colors.YELLOW,
                    bold=True,
                )

                typer.echo(f"    Bus          : {device.bus.name}")

                typer.echo(
                    "    Address      : "
                    + (hex(device.address) if device.address is not None else "N/A")
                )

                typer.echo("    Manufacturer : " + (device.manufacturer or "Unknown"))

                typer.echo(f"    Status       : {device.status.name}")

                if device.metadata:

                    for key, value in device.metadata.items():

                        typer.echo(f"    {key:<12} : {value}")

                typer.echo()

    # Health

    typer.secho(
        "Health Summary",
        fg=typer.colors.GREEN,
        bold=True,
    )

    typer.echo()

    if result is None:

        typer.secho(
            "QUICK REPORT",
            fg=typer.colors.YELLOW,
            bold=True,
        )

    elif result.success:

        typer.secho(
            "GOOD WITH WARNINGS",
            fg=typer.colors.GREEN,
            bold=True,
        )

    else:

        typer.secho(
            "FAILED",
            fg=typer.colors.RED,
            bold=True,
        )

    typer.echo()

    typer.echo("Generated:")

    typer.echo(datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"))
