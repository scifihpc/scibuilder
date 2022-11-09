#!/bin/bash

set -euo pipefail

if [[ -z ${BUILDER_UID+x} ]] ; then
  [[ "$#" -lt 2 ]] && echo "Need at least two arguments: BUILDER_UID and commands to run!" && exit 1
  BUILDER_UID=$1
  shift
fi


[[ "$#" -lt 1 ]] && echo "Need at least one command to run!" && exit 1

COMMANDS="$@"


[ "${BUILDER_UID}" -gt 0 ] 2> /dev/null || ( echo "BUILDER_UID=$BUILDER_UID is not an integer!" && exit 1 )

groupadd --gid $BUILDER_UID builder
useradd --create-home --gid=$BUILDER_UID --uid=$BUILDER_UID --shell /bin/bash builder
groupadd --gid 60000 portage
gpasswd --add builder portage > /dev/null

exec gosu builder $COMMANDS
