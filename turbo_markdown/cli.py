# -*- coding: utf-8 -*-

import os.path
import click
from turbo_markdown import run_server


@click.command()
def main(args=None):
    """Console script for turbo_markdown"""
    click.echo("Replace this message by putting your code into "
               "turbo_markdown.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    abspath = os.path.abspath('.')
    print abspath
    run_server(abspath)


if __name__ == "__main__":
    main()
