import click

from ebird.api import hotspot_observations

from . import args
from .base import save


@click.command()
@click.option('--codes', **args.CODES)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--provisional', **args.PROVISIONAL)
@click.option('--detail', **args.DETAIL)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(codes, back, max_results, locale, provisional, detail, out, indent):
    """Get recent observations from a list of hotspots."""
    save(out, hotspot_observations(
        codes, back, max_results, locale, provisional, detail), indent)


if __name__ == '__main__':
    cli()
