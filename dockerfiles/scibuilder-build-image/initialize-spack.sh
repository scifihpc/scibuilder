#!/bin/bash

[ "$#" -ne 2 ] && echo "Need two arguments: spack location and version !" && exit 1

FOLDER=$1
VERSION=$2

if [[ ! -d "$FOLDER" ]]; then
  git clone https://github.com/spack/spack.git "$FOLDER"
  cd "$FOLDER"
  git checkout "$VERSION"
else
  cd "$FOLDER"
  git reset "$VERSION"
fi

