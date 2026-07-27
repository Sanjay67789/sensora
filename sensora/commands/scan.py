"""
Scan command for Sensora.
"""

from __future__ import annotations

import json

import typer

from sensora.buses.linux.onewire import LinuxOneWireBus
from sensora.database.loader import DatabaseLoader
from sensora.database.matcher import DeviceMatcher
from sensora.discovery.i2c import I2CScanner
from sensora.discovery.onewire import OneWireScanner
from sensora.discovery.scanner import Scanner
from sensora.discovery.spi import SPIScanner
from sensora.discovery.uart import UARTScanner

app = typer.Typer(
    help="Scan the system for supported hardware devices.",
)


@app.callback(invoke_without_command=True)
def main(
    bus: str = typer.Option(
        "all",
        "--bus",
        "-b",
        help="Bus to scan (all, i2c, spi, uart, onewire).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output scan results as JSON.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output.",
    ),
) -> None:
    """
    Scan the system and display all detected hardware devices.
    """

    # Load device database
    registry = DatabaseLoader().load()

    # Create identification engine
    matcher = DeviceMatcher(registry)

    scanner = Scanner()

    match bus.lower():

        case "all":

            scanner.register(I2CScanner(matcher=matcher))

            scanner.register(SPIScanner())

            scanner.register(UARTScanner())

            scanner.register(OneWireScanner(LinuxOneWireBus()))

        case "i2c":

            scanner.register(I2CScanner(matcher=matcher))

        case "spi":

            scanner.register(SPIScanner())

        case "uart":

            scanner.register(UARTScanner())

        case "onewire":

            scanner.register(OneWireScanner(LinuxOneWireBus()))

        case _:

            typer.secho(
                f"Unsupported bus '{bus}'.",
                fg=typer.colors.RED,
            )

            raise typer.Exit(code=1)

    if verbose:

        typer.secho(
            "Scanning hardware...",
            fg=typer.colors.CYAN,
        )

    result = scanner.scan()

    devices = result.devices

    if json_output:

        output = []

        for device in devices:

            output.append(
                {
                    "name": device.name,
                    "bus": device.bus.name,
                    "manufacturer": device.manufacturer,
                    "address": (
                        hex(device.address) if device.address is not None else None
                    ),
                    "status": device.status.name,
                    "description": device.description,
                    "metadata": device.metadata,
                }
            )

        typer.echo(
            json.dumps(
                output,
                indent=4,
            )
        )

        return

    typer.echo()

    if not devices:

        typer.secho(
            "No supported devices found.",
            fg=typer.colors.YELLOW,
        )

        if verbose:

            for bus_result in result.buses:

                typer.echo(f"{bus_result.name}: {bus_result.message}")

        typer.echo(f"Scan completed in {result.duration:.3f} s")

        return

    typer.secho(
        f"Found {len(devices)} device(s)\n",
        fg=typer.colors.GREEN,
        bold=True,
    )

    for index, device in enumerate(
        devices,
        start=1,
    ):

        typer.echo(f"[{index}] {device.name}")

        typer.echo(f"    Bus          : {device.bus.name}")

        typer.echo(
            "    Address      : "
            + (hex(device.address) if device.address is not None else "N/A")
        )

        typer.echo("    Manufacturer : " + (device.manufacturer or "Unknown"))

        typer.echo(f"    Status       : {device.status.name}")

        if device.description:

            typer.echo(f"    Description  : {device.description}")

        if device.metadata:

            for key, value in device.metadata.items():

                typer.echo(f"    {key:<12} : {value}")

        typer.echo()

    typer.echo(f"Scan completed in {result.duration:.3f} s")
