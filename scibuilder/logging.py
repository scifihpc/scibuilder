# -*- coding: utf-8 -*-
import logging
import coloredlogs

def initializeLogger(loglevel='INFO'):
    """getLogger creates a logger.

    Args:
        loglevel (str): Loglevel to use. Default is 'INFO'.
    """

    loglevel = loglevel.upper()
    coloredlogs.install(
        level=loglevel,
        fmt='%(asctime)s %(hostname)s %(name)s %(levelname)s %(message)s'
    )
    logger = logging.getLogger()

    return logger
