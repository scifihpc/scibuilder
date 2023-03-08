# -*- coding: utf-8 -*-
import logging
import coloredlogs

def initializeLogger(loglevel='INFO'):
    """getLogger creates a logger.

    Args:
        loglevel (str): Loglevel to use. Default is 'INFO'.
    """
    loglevel = loglevel.upper()

    logger = logging.getLogger('Scibuilder')

    coloredlogs.install(
        fmt='%(asctime)s %(hostname)s %(name)s %(levelname)s %(message)s',
        level=loglevel
    )
