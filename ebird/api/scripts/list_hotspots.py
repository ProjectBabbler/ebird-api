import click

from ebird.api import list_hotspots

from . import args
from .base import save


@click.command()
@click.option('--code', **args.CODE)
@click.option('--back', **args.BACK)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(code, back, out, indent):
    """List all hotspots visited recently within a region."""
    save(out, list_hotspots(code, back), indent)

if __name__ == '__main__':
    cli()
