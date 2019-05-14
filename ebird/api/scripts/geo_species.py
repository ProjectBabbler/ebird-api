import click

from ebird.api import geo_species

from . import args
from .base import save


@click.command()
@click.option('--species', **args.SPECIES)
@click.option('--lat', **args.LATITUDE)
@click.option('--lng', **args.LONGITUDE)
@click.option('--dist', **args.BACK)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--provisional', **args.PROVISIONAL)
@click.option('--hotspot', **args.HOTSPOT)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(species, lat, lng, dist, back, max_results, locale, provisional, hotspot, out, indent):
    """Get most recent observation of a species nearby."""
    save(out, geo_species(species, lat, lng, dist, back, max_results, locale,
                          provisional, hotspot), indent)


if __name__ == '__main__':
    cli()
