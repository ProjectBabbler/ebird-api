import click

from ebird.api import nearest_species

from . import args
from .base import save


@click.command()
@click.option('--species', **args.SPECIES)
@click.option('--lat', **args.LATITUDE)
@click.option('--lng', **args.LONGITUDE)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--provisional', **args.PROVISIONAL)
@click.option('--hotspot', **args.HOTSPOT)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(species, lat, lng, back, max_results, locale, provisional, hotspot, out, indent):
    """Get the nearest, recent, observations of a species."""
    save(out, nearest_species(
        species, lat, lng, back, max_results, locale, provisional, hotspot), indent)

if __name__ == '__main__':
    cli()
