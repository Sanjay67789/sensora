"""
Report command for Sensora.
"""

import typer

app = typer.Typer(
    help="Generate hardware reports.",
)


@app.callback(invoke_without_command=True)
def main() -> None:
    """
    Generate hardware reports.
    """
    typer.echo("Report command is not implemented yet.")
