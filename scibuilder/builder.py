# -*- coding: utf-8 -*-
import os
import logging
from jsonschema import validate, Draft4Validator
from .utils import readYaml, formatYamlDict


def readConfig(conf_file, schema):
    conf = readYaml(conf_file)
    validate(instance=conf, schema=schema)
    return conf

class Builder:

    CONF_SCHEMA = {
        '$schema': 'http://json-schema.org/schema#',
        'title': 'Default configuration file schema',
        'type': 'object',
        'additionalProperties': True
    }

    def __init__(self, conf):
        self.conf = readConfig(conf, self.CONF_SCHEMA)
        self.logger = logging.getLogger('Scibuilder')
        self.logger.info("Configuration used:\n%s", formatYamlDict(self.conf))

    def build(self, tags=None):
        pass

    def deploy(self, tags=None):
        pass

    @staticmethod
    def check_tags(tags, env_tags):
        tag_found = False
        for tag in tags:
            if tag in env_tags:
                tag_found = True
        return tag_found
