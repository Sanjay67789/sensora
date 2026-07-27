"""
Command-line interface for Sensora.
"""

import typer

from sensora.commands.devices import app as devices_app
from sensora.commands.doctor import app as doctor_app
from sensora.commands.info import app as info_app
from sensora.commands.report import app as report_app
from sensora.commands.scan import app as scan_app

app = typer.Typer(
    name="sensora",
    help="Embedded Hardware Discovery, Diagnostics, and Management Framework.",
    no_args_is_help=True,
    add_completion=False,
)

app.add_typer(scan_app, name="scan")
app.add_typer(info_app, name="info")
app.add_typer(doctor_app, name="doctor")
app.add_typer(report_app, name="report")
app.add_typer(devices_app, name="devices")
