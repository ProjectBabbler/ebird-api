import click

from ebird.api import location_notable

from . import args
from .base import save


@click.command()
@click.option('--codes', **args.CODES)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--detail', **args.DETAIL)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(codes, back, max_results, locale, detail, out, indent):
    """Get recent observations of a rare species from a list of locations."""
    save(out, location_notable(
        codes, back, max_results, locale, detail), indent)


if __name__ == '__main__':
    cli()
