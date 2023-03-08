# -*- coding: utf-8 -*-
import os
import logging
from io import StringIO
from ruamel.yaml import YAML
from textwrap import indent
from jsonschema import validate, Draft4Validator


def read_config(conf_file, schema):
    yaml = YAML(typ='safe')
    with open(conf_file, 'r') as c_f:
        conf = yaml.load(c_f.read())
    validate(instance=conf, schema=schema)
    return conf

def format_config(conf):
    s = StringIO()
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.default_flow_style = False
    yaml.dump(conf, s)
    return indent(s.getvalue(), 4*' ')


class Builder:

    CONF_SCHEMA = {
        '$schema': 'http://json-schema.org/schema#',
        'title': 'Default configuration file schema',
        'type': 'object',
        'additionalProperties': True
    }

    def __init__(self, conf):
        self.conf = read_config(conf, self.CONF_SCHEMA)
        self.logger = logging.getLogger('Scibuilder')
        self.logger.info("Configuration used:\n%s", format_config(self.conf))

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
