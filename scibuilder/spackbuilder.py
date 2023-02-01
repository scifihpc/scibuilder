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

        envs = self.conf.get("environments", [])

        self.logger.info("Found %d environments.", len(envs))

        sysenv = dict(os.environ)

        def run_spack(env_file_dir, *commands):
            args = ["--env-dir", env_file_dir]
            args += list(commands)
            kwargs = {'_out':logging.info, '_err':logging.error, '_env':sysenv }
            spack(*args, **kwargs)

        def run_spack_capture(env_file, *commands):
            args = ["--env-dir", env_file_dir]
            args += list(commands)
            kwargs = {'_err':logging.error, '_env':sysenv }
            return spack(*args, **kwargs)

        for env in envs:

            assert 'name' in env, \
                f"Missing an environment name."

            name = env['name']

            assert 'environment_file' in env, \
                f"Environment {name} has no environment file."

            env_file = env['environment_file']

            env_file_abs = getAbsolutePath(env_file)
            env_file_dir, env_file_name = os.path.split(env_file_abs)

            assert env_file_name == "spack.yaml", \
                f"Environment file {env_file} is not named spack.yaml."

            assert os.path.isfile(env_file_abs), \
                f"Environment file {env_file_abs} does not exist!"

            self.logger.info("%s - Doing a reindex of installed packages", name)
            self.logger.info("%s - Currently installed packages", name)
            spack("--env-dir", env_file_dir, "find", _out=logging.info, _err=logging.error, _env=sysenv)

            compilers = env.get('compilers', [])

            self.logger.info("%s - Finding system compilers", name)
            spack("--env-dir", env_file_dir, "compiler", "find", _out=logging.info, _err=logging.error, _env=sysenv)
            for compiler in compilers:
                self.logger.info("%s - Installing compilers", name)
                spack("--env-dir", env_file_dir, "install", "--add", compiler, _out=logging.info, _err=logging.error, _env=sysenv)
                compiler_dir=str(spack("--env-dir", env_file_dir, "location", "-i", compiler, _err=logging.error, _env=sysenv)).strip()
                spack("--env-dir", env_file_dir, "compiler", "add", compiler_dir, _out=logging.info, _err=logging.error, _env=sysenv)

            self.logger.info("%s - Listing compilers", name)
            spack("--env-dir", env_file_dir, "compilers", _out=logging.info, _err=logging.error, _env=sysenv)

            self.logger.info("%s - Concretizing build", name)
            spack("--env-dir", env_file_dir, "concretize", _out=logging.info, _err=logging.error, _env=sysenv)

            self.logger.info("%s - Starting build", env_file)
            spack("--env-dir", env_file_dir, "install", _out=logging.info, _err=logging.error, _env=sysenv)

            #self.logger.info("%s - Refreshing modules", env_file)
            #spack("--env-dir", env_file_dir, "--debug", "module", "lmod", "refresh", "--delete-tree", _out=logging.info, _err=logging.error, _env=sysenv)


