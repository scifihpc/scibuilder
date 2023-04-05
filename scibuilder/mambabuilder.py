# -*- coding: utf-8 -*-
import os
import logging
from .builder import Builder
from .utils import (getAbsolutePath,
                    calculateChecksum,
                    calculateEnvChecksum,
                    assertGetValue,
                    assertPathName,
                    downloadFile)
import sh
import shutil
import copy

class MambaBuilder(Builder):


    def build(self, tags=None):

        envs = self.conf.get("environments", [])
        installers = self.conf.get("installers", [])

        self.logger.info("Found %d environments.", len(envs))

        envs = self.conf.get("environments", [])

        sysenv = dict(os.environ)


        def run_installer(installer, build_env, *commands):

            kwargs = {'_out':logging.info, '_err':logging.error, '_env':build_env }

            cmd = sh.Command(installer)
            cmd(*commands, **kwargs)


        for env in envs:

            name = assertGetValue(env, 'name', "Missing an environment name.")

            env_file = assertGetValue(env, 'environment_file', f"Environment {name} has no environment file.")

            conf_path = os.path.dirname(self.conf['conf_file'])

            env_file_abs = getAbsolutePath(env_file, base_dir=conf_path)

            assert os.path.isfile(env_file_abs), \
                f"Environment file {env_file_abs} does not exist!"

            installer_name =  assertGetValue(env, 'installer', f"Environment {name} has no installer.")

            install_path =  os.path.join(assertGetValue(env, 'install_prefix', f"Environment {name} has no install prefix."), name)
            module_path =  os.path.join(assertGetValue(env, 'module_prefix', f"Environment {name} has no module prefix."), name)

            assertPathName(install_path, "Installation path (install_prefix + name) can only contain letters, numbers, underscores and dashes.")
            assertPathName(module_path, "Module path (module_prefix + name) can only contain letters, numbers, underscores and dashes.")

            installer =  assertGetValue(installers, installer_name, f"Installer {installer_name} is not specified.")

            url = assertGetValue(installer, 'url', f"Installer {installer_name} does not have a url.")

            checksum = assertGetValue(installer, 'sha256sum', f"Installer {installer_name} does not have a checksum.")

            cache_path = assertGetValue(installer, 'cache_path', f"Installer {installer_name} does not have a cache path.")

            installer_archive = os.path.join(cache_path, assertGetValue(installer, 'installer_archive', f"Installer {installer_name} does not have a filename."))

            installer_binary = os.path.join(cache_path, assertGetValue(installer, 'installer_binary', f"Installer {installer_name} does not have a filename."))

            build_env = copy.deepcopy(sysenv)
            build_env.update(env.get('build_environment', {}))

            hash_length = env.get('hash_length', None)
            if hash_length:
                try:
                    hash_length = int(hash_length)
                except ValueError as e:
                    self.logger.error(f'Hash length "{hash_length}" is not an integer!')
                    raise e

            if not os.path.isfile(installer_binary):
                self.logger.info(f"Could not find installer {installer_binary}. Trying to download it.")
                if not os.path.isfile(installer_archive):
                    self.logger.info(f"Downloading installer archive {installer_archive} from {url}")
                    downloadFile(url, installer_archive)
                self.logger.info(f"Calculating sha256 checksum for installer {installer_archive}.")

                calculated_checksum = calculateChecksum(installer_archive)
                assert checksum == calculated_checksum, \
                    f"Archive checksum does not match: {checksum} != {calculated_checksum} !"

                self.logger.info(f"Extracting {installer_archive}.")
                sh.tar("-C", cache_path, "-x", "-f", installer_archive)

            env_checksum = calculateEnvChecksum(env_file_abs, length=hash_length)

            if not os.path.isdir(install_path):
                self.logger.info(f"Creating base install path: {install_path}")
                os.makedirs(install_path)

            if hash_length:
                install_path = os.path.join(install_path, env_checksum)

            installed_env_file = os.path.join(install_path, 'environment.yml')

            if not os.path.isfile(installed_env_file):
                self.logger.info(f"Environment {name} does not exist. Starting installation.")
                run_installer(installer_binary,
                              build_env,
                              "env", "create",
                              "--no-allow-softlinks",
                              "--no-rc",
                              "--no-env",
                              "--yes",
                              "--prefix", install_path,
                              "--file", env_file_abs)
                self.logger.info(f"Installation of environment {name} was successful. Copying environment file.")
                shutil.copyfile(env_file_abs, installed_env_file)

            else:
                self.logger.info(f"Environment {name} exists, not installing.")
