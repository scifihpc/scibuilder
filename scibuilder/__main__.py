# -*- coding: utf-8 -*-
import os
import logging
import click
from scibuilder.spackbuilder import SpackBuilder
from scibuilder.logging import initializeLogger


@click.command()
@click.argument("builder", type=click.Choice(("spack", "conda", "singularity")), nargs=1)
@click.argument("command", type=click.Choice(("build", "deploy")), nargs=1)
@click.argument("conf", type=str, nargs=1)
@click.option("--loglevel", default="info", type=click.Choice(("debug", "info", "warning")))
@click.option("--cwd", default=None, help="Change working directory")
@click.option("--tags", default=None, help="Only build environments with these tags")
def run_builder(builder, command, conf, loglevel, cwd, tags):

    initializeLogger(loglevel)

    logger = logging.getLogger('Scibuilder')

    if tags is not None:
        tags = str(tags).split(',')
        logger.info(f"Tags specified: {tags}")

    if cwd is not None:
        logger.info(f"Switching working directory from {os.getcwd()} to {cwd}")
        os.chdir(cwd)

    builders = {
        "spack": SpackBuilder,
        "conda": None,
        "singularity": None,
    }
    builder = builders[builder](conf)

    if command == "build":
        try:
            builder.build(tags=tags)
        except Exception as e:
            logger.error("Build step produced an error:\n\n%s", str(e))
            raise e


if __name__=="__main__":
    run_builder()
