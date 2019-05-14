import click

from ebird.api import find_regions

from ebird.api.scripts import args
from ebird.api.scripts.base import save


@click.command()
@click.option('--rtype', **args.REGION_TYPE)
@click.option('--match', **args.MATCH)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(rtype, match, out, indent):
    """Find matching regions."""
    save(out, find_regions(rtype, match), indent)


if __name__ == '__main__':
    cli()
