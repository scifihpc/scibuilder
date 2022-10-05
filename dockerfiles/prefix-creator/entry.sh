#!/bin/bash

set -euo pipefail

[ "$#" -ne 2 ] && echo "Need two arguments: EPREFIX and BUILDER_UID!" && exit 1

EPREFIX="$1"
BUILDER_UID="$2"

[ ! -d ${EPREFIX} ] && echo "No directory found for EPREFIX=${EPREFIX}" && exit 1

[ -z ${BUILDER_UID+x} ] && echo "BUILDER_UID is not set!" && exit 1

[ "${BUILDER_UID}" -gt 0 ] 2> /dev/null || ( echo "BUILDER_UID=$BUILDER_UID is not an integer!" && exit 1 )

useradd --create-home --uid=$BUILDER_UID --shell /bin/bash builder
groupadd --gid 60000 portage
gpasswd --add builder portage > /dev/null

while true; do
    read -p "Will chown ${EPREFIX} to UID ${BUILDER_UID}. Is this ok? [Y/n]" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) break;;
    esac
done

chown -Rh $BUILDER_UID.$BUILDER_UID ${EPREFIX}

exec gosu builder /usr/local/bin/bootstrap-helper.sh "${EPREFIX}"
