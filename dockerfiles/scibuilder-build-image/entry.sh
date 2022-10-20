#!/bin/bash

set -euo pipefail

[ "$#" -lt 2 ] && echo "Need at least two arguments: BUILDER_UID and commands to run!" && exit 1

BUILDER_UID=$1
COMMANDS="${@:2}"

[ -z ${BUILDER_UID+x} ] && echo "BUILDER_UID is not set!" && exit 1

[ "${BUILDER_UID}" -gt 0 ] 2> /dev/null || ( echo "BUILDER_UID=$BUILDER_UID is not an integer!" && exit 1 )

groupadd --gid $BUILDER_UID builder
useradd --create-home --gid=$BUILDER_UID --uid=$BUILDER_UID --shell /bin/bash builder
groupadd --gid 60000 portage
gpasswd --add builder portage > /dev/null

exec gosu builder $COMMANDS
