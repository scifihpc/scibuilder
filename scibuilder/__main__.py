# -*- coding: utf-8 -*-
import click
from scibuilder.spackbuilder import SpackBuilder
from scibuilder.logging import initializeLogger


@click.command()
@click.argument("builder", type=click.Choice(("spack", "conda", "singularity")), nargs=1)
@click.argument("command", type=click.Choice(("build", "deploy")), nargs=1)
@click.argument("conf", type=click.Path(exists=True), nargs=1)
@click.option("--loglevel", default="info", type=click.Choice(("debug", "info", "warning")))
def run_builder(builder, command, conf, loglevel):

    logger = initializeLogger(loglevel)

    builders = {
        "spack": SpackBuilder,
        "conda": None,
        "singularity": None,
    }
    builder = builders[builder](conf)

    if command == "build":
        try:
            builder.build()
        except Exception as e:
            logger.error("Build step produced an error:\n\n%s", str(e))
            raise e


if __name__=="__main__":
    run_builder()
