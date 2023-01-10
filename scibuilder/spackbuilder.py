# -*- coding: utf-8 -*-
import os
import sys
import logging
import pprint
from .builder import Builder

try:
    from sh import spack
except ImportError as e:
    logging.error("Spack was not found. Spack builder will not work.")


def getAbsolutePath(path):
    if path[0] != '/':
        workdir = os.getcwd()
        path = os.path.join(workdir, path)
    return path


class SpackBuilder(Builder):

    def build(self):

        env_files = self.conf.get("environment_files", [])

        self.logger.info("Found %d environments.", len(env_files))

        for env_file in env_files:

            env_file_abs = getAbsolutePath(env_file)
            env_file_dir, env_file_name = os.path.split(env_file_abs)

            assert env_file_name == "spack.yaml", \
                f"Environment file {env_file} is not named spack.yaml."

            assert os.path.isfile(env_file_abs), \
                f"Environment file {env_file_abs} does not exist!"

            sysenv = dict(os.environ)

            self.logger.info("Concretizing build for %s", env_file)
            spack("--env-dir", env_file_dir, "concretize", _out=logging.info, _err=logging.error, _env=sysenv)
            self.logger.info("Starting build for %s", env_file)
            spack("--env-dir", env_file_dir, "install", _out=logging.info, _err=logging.error, _env=sysenv)


