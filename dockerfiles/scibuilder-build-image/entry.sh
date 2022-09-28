#!/bin/bash

set -euo pipefail

BUILDER_UID=$1

useradd --create-home --uid=$BUILDER_UID --shell /bin/bash builder
groupadd --gid 60000 portage
gpasswd --add builder portage > /dev/null

exec gosu builder /bin/bash
