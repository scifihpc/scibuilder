#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo 'Need a path to gentoo prefix'
    exit 1
fi

export EPREFIX=$1
export BOOTSTRAP_DATE=$(date -Idate)

mkdir -p ${EPREFIX}
cd ${EPREFIX}
if [ ! -f bootstrap-prefix.sh ]; then
    wget https://gitweb.gentoo.org/repo/proj/prefix.git/plain/scripts/bootstrap-prefix.sh
    chmod +x bootstrap-prefix.sh
fi
echo ${BOOTSTRAP_DATE} > bootstrap-date.log


BUILDER_UID=$(id -u)
chown -Rh $BUILDER_UID.$BUILDER_UID ${EPREFIX}

export PATH="${EPREFIX}/usr/bin:${EPREFIX}/bin:${EPREFIX}/tmp/usr/bin:${EPREFIX}/tmp/bin:$PATH"
${EPREFIX}/bootstrap-prefix.sh ${EPREFIX} noninteractive | tee bootstrap.log
