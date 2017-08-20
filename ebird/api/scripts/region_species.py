import click

from ebird.api import region_species

from . import args
from .base import save


@click.command()
@click.option('--species', **args.SPECIES)
@click.option('--code', **args.CODE)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--provisional', **args.PROVISIONAL)
@click.option('--hotspot', **args.HOTSPOT)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(species, code, back, max_results, locale, provisional, hotspot, out, indent):
    """Get recent observations for a given species in a region."""
    save(out, region_species(
        species, code, back, max_results, locale, provisional, hotspot), indent)

if __name__ == '__main__':
    cli()
