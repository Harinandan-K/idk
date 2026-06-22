import typer
from rich import print

idk_cli = typer.Typer(name='IDK-CLI')

@idk_cli.command()
def fetch_history():
    print('hi')


def run() -> None:
    idk_cli()