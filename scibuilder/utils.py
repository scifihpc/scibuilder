# -*- coding: utf-8 -*-
import os
import re
import hashlib
import requests
import json
from io import StringIO
from textwrap import indent
from ruamel.yaml import YAML


def readYaml(filename):
    yaml = YAML(typ='safe')
    with open(filename, 'r') as f:
        yaml_output = yaml.load(f.read())
    return yaml_output


def formatYamlDict(d):
    s = StringIO()
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.default_flow_style = False
    yaml.dump(d, s)
    return indent(s.getvalue(), 4*' ')


def getAbsolutePath(path, base_dir=None):
    if path[0] == '/':
        return path

    if not base_dir:
        base_dir = os.getcwd()

    return os.path.realpath(os.path.join(base_dir, path))


def assertGetValue(d, k, msg):
    assert k in d, msg
    return d[k]


def assertPathName(path, msg):
    search = re.match('^(/[a-zA-Z0-9_-]+)+$', path)
    assert search is not None, msg


def downloadFile(url, filename):
    folder = os.path.dirname(filename)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    with open(filename, 'wb') as f:
        result = requests.get(url, allow_redirects=True)
        f.write(result.content)


def calculateChecksum(filename, hash_function='sha256'):
    hash_functions = {
        'sha256': hashlib.sha256
    }
    hash_function = hash_functions[hash_function]()
    with open(filename, "rb") as input_file:
        for byte_block in iter(lambda: input_file.read(4096), b""):
            hash_function.update(byte_block)

    return hash_function.hexdigest()


def calculateEnvChecksum(environment_file, length=None, hash_function='sha256'):
    env_dict = formatYamlDict(readYaml(environment_file))

    hash_functions = {
        'sha256': hashlib.sha256
    }
    hash_function = hash_functions[hash_function]()
    json_dump = json.dumps(env_dict, ensure_ascii=False, sort_keys=True)
    hash_function.update(json_dump.encode('utf-8'))

    digest = hash_function.hexdigest()
    if length:
        digest = digest[:length]
    return digest
