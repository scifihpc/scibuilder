# Build the prefix builder container

Prefix builder container can be built with the following commands.

Alma 9:
```sh
docker build -t aaltoscienceit/prefix-creator:alma9 -f Dockerfile.alma9 .
```

Ubuntu 22.04
```sh
docker build -t aaltoscienceit/prefix-creator:ubuntu22.04 -f Dockerfile.ubuntu22.04 .
```

# Running the prefix builder container

Create a folder where the prefix will be built. One needs to have sudo rights to this folder so that one can `chown` the folder for the builder id.

```sh
EPREFIX=/appl/prefix/2022-09
LOCAL_FOLDER=/tmp/$EPREFIX
mkdir $LOCAL_FOLDER
```

The container takes two arguments: `$EPREFIX` and `$BUILDER_UID` that tell where the prefix should be built and what UID should be used to build it.

An easy test is to run the builder with the following commands:
```sh
EPREFIX=/appl/prefix/2022-09
BUILDER_UID=$(id -u)
BUILDER_OS=alma9
docker run -v $LOCAL_FOLDER:$EPREFIX --rm -it aaltoscienceit/prefix-creator:$BUILDER_OS $EPREFIX $BUILDER_UID
```

This will create a Gentoo prefix to `/tmp/appl/prefix/2022-09` with you UID.
Code will ask for confirmation on whether it should `chown` everything in `$EPREFIX` to user `$BUILDER_UID`.
This is needed as otherwise Gentoo prefix will try to install into the home folder of the builder user.
