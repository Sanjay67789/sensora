"""
Scan command for Sensora.
"""

from __future__ import annotations

import json

import typer

from sensora.discovery.i2c import I2CScanner
from sensora.discovery.scanner import Scanner

app = typer.Typer(
    help="Scan the system for supported hardware devices.",
)


@app.callback(invoke_without_command=True)
def main(
    bus: str = typer.Option(
        "all",
        "--bus",
        "-b",
        help="Bus to scan (all, i2c).",
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

    scanner = Scanner()

    match bus.lower():
        case "all":
            scanner.register(I2CScanner())

        case "i2c":
            scanner.register(I2CScanner())

        case _:
            typer.secho(
                f"Unsupported bus '{bus}'.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)

    if verbose:
        typer.secho("Scanning hardware...", fg=typer.colors.CYAN)

    result = scanner.scan()

    if json_output:
        output = []

        for device in result.devices:
            output.append(
                {
                    "name": device.name,
                    "bus": device.bus.name,
                    "manufacturer": device.manufacturer,
                    "address": (
                        hex(device.address)
                        if device.address is not None
                        else None
                    ),
                    "status": device.status.name,
                    "description": device.description,
                }
            )

        typer.echo(json.dumps(output, indent=4))
        return

    typer.echo()

    if not result.devices:
        typer.secho(
            "No supported devices found.",
            fg=typer.colors.YELLOW,
        )

        typer.echo(f"Scan completed in {result.duration:.3f} s")
        return

    typer.secho(
        f"Found {result.device_count} device(s)\n",
        fg=typer.colors.GREEN,
        bold=True,
    )

    for index, device in enumerate(result.devices, start=1):
        typer.echo(f"[{index}] {device.name}")
        typer.echo(f"    Bus          : {device.bus.name}")

        typer.echo(
            "    Address      : "
            + (
                hex(device.address)
                if device.address is not None
                else "N/A"
            )
        )

        typer.echo(
            "    Manufacturer : "
            + (device.manufacturer or "Unknown")
        )

        typer.echo(
            f"    Status       : {device.status.name}"
        )

        if device.description:
            typer.echo(
                f"    Description  : {device.description}"
            )

        typer.echo()

    typer.echo(f"Scan completed in {result.duration:.3f} s")
