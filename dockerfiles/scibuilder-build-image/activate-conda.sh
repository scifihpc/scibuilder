#!/bin/bash

set -eo pipefail

[ "$#" -lt 1 ] && echo "Need at least one command to run!" && exit 1

COMMANDS="${@}"

echo "Activating conda environment from /opt/conda/bin"
export PATH=/opt/conda/bin:$PATH

cd /scibuilder

/bin/bash -c "$COMMANDS"
