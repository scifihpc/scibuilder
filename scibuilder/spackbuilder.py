# -*- coding: utf-8 -*-
import os
import sys
import copy
import logging
import pprint
from .builder import Builder
from .utils import getAbsolutePath

try:
    import sh
    from sh import spack
except ImportError as e:
    logging.error("Spack was not found. Spack builder will not work.")



class SpackBuilder(Builder):

    def build(self, tags=None):

        envs = self.conf.get("environments", [])

        self.logger.info("Found %d environments.", len(envs))

        sysenv = dict(os.environ)


        for env in envs:

            assert 'name' in env, \
                f"Missing an environment name."

            name = env['name']

            assert 'environment_file' in env, \
                f"Environment {name} has no environment file."

            env_file = env['environment_file']

            conf_path = os.path.dirname(self.conf['conf_file'])

            env_file_abs = getAbsolutePath(env_file, base_dir=conf_path)
            env_file_dir, env_file_name = os.path.split(env_file_abs)

            assert env_file_name == "spack.yaml", \
                f"Environment file {env_file} is not named spack.yaml."

            assert os.path.isfile(env_file_abs), \
                f"Environment file {env_file_abs} does not exist!"

            build_environment = env.get('build_environment', {})

            build_env = copy.deepcopy(sysenv)
            build_env.update(build_environment)

            def run_spack(*commands):
                args = ["--env-dir", env_file_dir]
                args += list(commands)
                kwargs = {'_out':logging.info, '_err':logging.error, '_env':build_env }
                spack(*args, **kwargs)

            def run_spack_capture(*commands):
                args = ["--env-dir", env_file_dir]
                args += list(commands)
                kwargs = {'_err':logging.error, '_env':build_env }
                return spack(*args, **kwargs)

            if tags is not None:
                env_tags = env.get('tags', [])
                if not self.check_tags(tags, env_tags):
                    self.logger.info("%s - Environment not tagged for building", name)
                    continue

            self.logger.info("%s - Doing a reindex of installed packages", name)
            self.logger.info("%s - Currently installed packages", name)
            run_spack("find")

            system_compiler = env.get('system_compiler', "")
            compilers = env.get('compilers', [])

            self.logger.info("%s - Finding system compilers", name)
            run_spack("compiler", "find")
            for compiler in compilers:

                compiler_spec = f"{compiler}%{system_compiler}"

                tries = 0
                compiler_found = False
                while tries < 2 and not compiler_found:
                    self.logger.info("%s - Checking if compiler %s is present", name, compiler_spec)
                    try:
                        compiler_find = run_spack_capture("find", compiler_spec)
                        compiler_found = True
                    except sh.ErrorReturnCode:
                        pass

                    if not compiler_found:
                        self.logger.info("%s - Installing compiler %s", name, compiler_spec)
                        run_spack("install", "--add", compiler_spec)
                    else:
                        compiler_dir=str(run_spack_capture("location", "-i", compiler_spec)).strip()
                        run_spack("compiler", "find", compiler_dir)

                    tries += 1


            self.logger.info("%s - Listing compilers", name)
            run_spack("compilers")

            self.logger.info("%s - Concretizing build", name)
            run_spack("concretize")

            self.logger.info("%s - Starting build", env_file)
            run_spack("install")

            self.logger.info("%s - Rebuilding modules", env_file)
            run_spack("module", "lmod", "refresh", "-y")
