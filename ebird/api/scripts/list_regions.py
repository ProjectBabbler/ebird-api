import click

from ebird.api import list_regions

from . import args
from .base import save

# TODO Add validation for the combination of rtype and code. see list_regions().

@click.command()
@click.option('--rtype', **args.REGION_TYPE)
@click.option('--code', **args.CODE_OPTIONAL)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(rtype, code, out, indent):
    """List all regions."""
    save(out, list_regions(rtype, code), indent)

if __name__ == '__main__':
    cli()
