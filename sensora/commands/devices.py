"""
Devices command for Sensora.
"""

from __future__ import annotations

import typer

from sensora.database.exceptions import SchemaValidationError
from sensora.database.loader import DatabaseLoader

app = typer.Typer(
    help="Show supported Sensora devices.",
)


@app.callback(invoke_without_command=True)
def main(
    vendor: str | None = typer.Option(
        None,
        "--vendor",
        "-v",
        help="Filter devices by vendor.",
    ),
    bus: str | None = typer.Option(
        None,
        "--bus",
        "-b",
        help="Filter devices by interface/bus.",
    ),
    category: str | None = typer.Option(
        None,
        "--category",
        "-c",
        help="Filter devices by category.",
    ),
) -> None:
    """
    Display supported Sensora devices.
    """

    try:
        registry = DatabaseLoader().load()

    except SchemaValidationError as exc:
        typer.secho(
            f"Failed to load device database: {exc}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1) from exc

    devices = list(registry.devices)

    if vendor:
        devices = [
            device for device in devices if device.vendor.lower() == vendor.lower()
        ]

    if bus:
        devices = [
            device
            for device in devices
            if bus.lower() in [interface.lower() for interface in device.interfaces]
        ]

    if category:
        devices = [
            device
            for device in devices
            if device.metadata.get(
                "category",
                "",
            ).lower()
            == category.lower()
        ]

    typer.echo()

    typer.secho(
        "Sensora Device Database",
        fg=typer.colors.CYAN,
        bold=True,
    )

    typer.echo()

    typer.echo(f"Vendors : {registry.vendor_count}")

    typer.echo(f"Devices : {len(devices)}")

    typer.echo()

    if not devices:
        typer.secho(
            "No matching devices found.",
            fg=typer.colors.YELLOW,
        )
        return

    for index, device in enumerate(
        devices,
        start=1,
    ):
        typer.secho(
            f"[{index}] {device.name}",
            fg=typer.colors.GREEN,
            bold=True,
        )

        typer.echo(f"    ID          : {device.id}")

        typer.echo(f"    Vendor      : {device.vendor}")

        if device.description:
            typer.echo(f"    Description : {device.description}")

        if device.interfaces:
            typer.echo("    Interfaces  : " + ", ".join(device.interfaces))

        typer.echo()
