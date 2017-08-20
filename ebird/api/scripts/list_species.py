import click

from ebird.api import list_species

from . import args
from.base import save

# TODO Add validation for the combination of rtype and code. see list_regions().


@click.command()
@click.option('--category', **args.CATEGORY)
@click.option('--locale', **args.LOCALE)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(category, locale, out, indent):
    """Get the list of species in the eBird taxonomy."""
    save(out, list_species(category, locale), indent)

if __name__ == '__main__':
    cli()
