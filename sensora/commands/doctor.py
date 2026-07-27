"""
Doctor command for Sensora.
"""

import typer

app = typer.Typer(
    help="Run hardware diagnostics.",
)


@app.callback(invoke_without_command=True)
def main() -> None:
    """
    Run hardware diagnostics.
    """
    typer.echo("Doctor command is not implemented yet.")
