import click

from ebird.api import geo_notable

from . import args
from .base import save


@click.command()
@click.option('--lat', **args.LATITUDE)
@click.option('--lng', **args.LONGITUDE)
@click.option('--dist', **args.BACK)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--hotspots', **args.HOTSPOT)
@click.option('--detail', **args.DETAIL)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(lat, lng, dist, back, max_results, locale, hotspots, detail, out, indent):
    """Get the nearby, recent observations of rare species."""
    save(out, geo_notable(lat, lng, dist, back, max_results, locale,
                          hotspots, detail), indent)


if __name__ == '__main__':
    cli()
