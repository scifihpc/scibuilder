#!/bin/bash

set -euo pipefail

if [[ -z ${BUILDER_UID+x} ]] ; then
  [[ "$#" -lt 2 ]] && echo "Need at least two arguments: BUILDER_UID and commands to run!" && exit 1
  BUILDER_UID=$1
  shift
fi

if [[ "$#" -lt 1 ]] ; then
  COMMANDS="tail -f /dev/null"
else
  COMMANDS="$@"
fi

[ "${BUILDER_UID}" -gt 0 ] 2> /dev/null || ( echo "BUILDER_UID=$BUILDER_UID is not an integer!" && exit 1 )

if [[ ! -z ${SKIP_ENTRY+x} ]]; then
  echo 'Skipping entry'
  exec " $COMMANDS"
fi

# Find builder user
set +e
id $BUILDER_UID &> /dev/null
USER_CHECK="$?"
set -e
if [[ "$USER_CHECK" -ne 0 ]] ; then
  echo "Builder user does not exist. Creating builder-user."
  groupadd --gid $BUILDER_UID builder
  useradd --create-home --gid=$BUILDER_UID --uid=$BUILDER_UID --shell /bin/bash builder
  groupadd --gid 60000 portage
  gpasswd --add builder portage > /dev/null
fi

echo "My ID is: "$(id)
echo "Builder user ID is: "$(id $BUILDER_UID)

exec gosu builder $COMMANDS
