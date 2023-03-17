# -*- coding: utf-8 -*-
import os
import logging
from .builder import Builder
from .utils import getAbsolutePath, calculateChecksum, calculateEnvChecksum, assertGetValue, downloadFile
import sh
import shutil

class MambaBuilder(Builder):


    def build(self, tags=None):

        envs = self.conf.get("environments", [])
        installers = self.conf.get("installers", [])

        self.logger.info("Found %d environments.", len(envs))

        envs = self.conf.get("environments", [])

        sysenv = dict(os.environ)


        def run_installer(installer, *commands):

            kwargs = {'_out':logging.info, '_err':logging.error, '_env':sysenv }

            cmd = sh.Command(installer)
            cmd(*commands, **kwargs)


        for env in envs:

            name = assertGetValue(env, 'name', "Missing an environment name.")

            env_file = assertGetValue(env, 'environment_file', f"Environment {name} has no environment file.")

            installer_name =  assertGetValue(env, 'installer', f"Environment {name} has no installer.")

            install_path =  assertGetValue(env, 'install_path', f"Environment {name} has no install path.")

            installer =  assertGetValue(installers, installer_name, f"Installer {installer_name} is not specified.")

            url = assertGetValue(installer, 'url', f"Installer {installer_name} does not have a url.")

            checksum = assertGetValue(installer, 'sha256sum', f"Installer {installer_name} does not have a checksum.")

            cache_path = assertGetValue(installer, 'cache_path', f"Installer {installer_name} does not have a cache path.")

            installer_archive = os.path.join(cache_path, assertGetValue(installer, 'installer_archive', f"Installer {installer_name} does not have a filename."))

            installer_binary = os.path.join(cache_path, assertGetValue(installer, 'installer_binary', f"Installer {installer_name} does not have a filename."))

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

            env_checksum = calculateEnvChecksum(env_file, length=hash_length)

            if not os.path.isdir(install_path):
                self.logger.info(f"Creating base install path: {install_path}")
                os.makedirs(install_path)

            if hash_length:
                install_path = os.path.join(install_path, env_checksum)


            installed_env_file = os.path.join(install_path, 'environment.yml')

            if not os.path.isfile(installed_env_file):
                self.logger.info(f"Environment {name} does not exist. Starting installation.")
                run_installer(installer_binary,
                              "env", "create",
                              "--no-allow-softlinks",
                              "--no-rc",
                              "--no-env",
                              "--yes",
                              "--prefix", install_path,
                              "--file", env_file)
                self.logger.info(f"Installation of environment {name} was successful. Copying environment file.")
                shutil.copyfile(env_file, installed_env_file)

            else:
                self.logger.info(f"Environment {name} exists, not installing.")
