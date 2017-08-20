import click

from ebird.api import nearest_hotspots

from . import args
from .base import save


@click.command()
@click.option('--lat', **args.LATITUDE)
@click.option('--lng', **args.LONGITUDE)
@click.option('--dist', **args.BACK)
@click.option('--back', **args.BACK)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(lat, lng, dist, back, out, indent):
    """Get the list of nearby hotspots."""
    save(out, nearest_hotspots(lat, lng, dist, back), indent)

if __name__ == '__main__':
    cli()
