#!/bin/bash

set -eo pipefail

[ "$#" -lt 1 ] && echo "Need at least one command to run!" && exit 1

COMMANDS="${@}"

if [ ! -d $HOME/.spack ]; then
  echo "Linking $HOME/.spack/bootstrap to /cache/spack_bootstrap"
  mkdir -p $HOME/.spack
  mkdir -p /cache/spack_bootstrap
  ln -s -T /cache/spack_bootstrap $HOME/.spack/bootstrap
fi

echo "Activating conda environment from /opt/conda/bin"
export PATH=/opt/conda/bin:$PATH
echo "Activating spack from /spack"
source /spack/share/spack/setup-env.sh

cd /scibuilder

/bin/bash -c "$COMMANDS"
