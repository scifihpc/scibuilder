#!/bin/bash

set -eo pipefail

[ "$#" -lt 2 ] && echo "Need at least two arguments: EPREFIX and commands!" && exit 1

EPREFIX="$1"
COMMANDS="${@:2}"

[ ! -d ${EPREFIX} ] && echo "No directory found for EPREFIX=${EPREFIX}" && exit 1

echo "Linking $HOME/.spack/bootstrap to /cache/spack_bootstrap"
mkdir -p $HOME/.spack
mkdir -p /cache/spack_bootstrap
ln -s -T /cache/spack_bootstrap $HOME/.spack/bootstrap

RETAIN="HOME=$HOME TERM=$TERM USER=$USER SHELL=$SHELL"

cat > /tmp/startprefix_minimal << EOF
#!$EPREFIX/bin/bash

echo "Activating gentoo prefix from ${EPREFIX}"
echo "Activating conda environment from /opt/conda/bin"
export PATH=/opt/conda/bin:\$PATH
echo "Activating spack from /spack"
source /spack/share/spack/setup-env.sh

cd /scibuilder

$EPREFIX/bin/bash -c "$COMMANDS"

EOF

$EPREFIX/usr/bin/env -i $RETAIN ${EPREFIX}/bin/bash /tmp/startprefix_minimal
