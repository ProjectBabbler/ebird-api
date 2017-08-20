import click

from ebird.api import region_notable

from . import args
from .base import save


@click.command()
@click.option('--code', **args.CODE)
@click.option('--back', **args.BACK)
@click.option('--max-results', **args.MAX_RESULTS)
@click.option('--locale', **args.LOCALE)
@click.option('--hotspot', **args.HOTSPOT)
@click.option('--detail', **args.DETAIL)
@click.option('--out', **args.OUT)
@click.option('--indent', **args.INDENT)
def cli(code, back, max_results, locale, hotspot, detail, out, indent):
    """Get recent observations of a rare species for a region."""
    save(out, region_notable(
        code, back, max_results, locale, hotspot, detail), indent)

if __name__ == '__main__':
    cli()
