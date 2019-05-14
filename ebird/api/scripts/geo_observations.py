import click

from ebird.api import geo_observations

from . import args
from .base import save


@click.command()
@click.option('--lat', **args.LATITUDE)
@click.option('--lng', **args.LONGITUDE)
@click.option('--dist', **args.BACK)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--provisional', **args.PROVISIONAL)
@click.option('--hotspots', **args.HOTSPOT)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(lat, lng, dist, back, max_results, locale, provisional, hotspots, out, indent):
    """Get nearby recent observations of each species."""
    save(out, geo_observations(lat, lng, dist, back, max_results, locale,
                               provisional, hotspots), indent)


if __name__ == '__main__':
    cli()
