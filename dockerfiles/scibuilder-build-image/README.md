# Build the build images

Build images can be built with the following commands.

Aalto Centos 7:
```sh
docker build -t aaltoscienceit/scibuilder-build-image:aalto-centos7 -f Dockerfile.aalto-centos7 .
```

HY Alma 8:
```sh
docker build -t aaltoscienceit/scibuilder-build-image:hy-alma8 -f Dockerfile.hy-alma8 .
```

# Requirements for a build

The build container expects the following things to be present:

- Gentoo prefix should be installed in a directory inside the container
- The place where the end product goes should be mounted inside the container
- Spack repository should be mounted on /spack inside the container
- Scibuilder repository should be mounted on /scibuilder
- Cache folder should be mounted in /cache

In the next example we use the following folder structure:
- `$LOCAL_FOLDER` - Root folder for other folders
- `$LOCAL_FOLDER/appl/prefix` - Root folder for Gentoo prefix installations
- `$LOCAL_FOLDER/appl/spack` - Root folder for Spack installation artifacts
- `$LOCAL_FOLDER/spack`- Spack repository
- `$LOCAL_FOLDER/scibuilder`- Scibuilder repository
- `$LOCAL_FOLDER/cache`- Cache repository

The `$LOCAL_FOLDER` should be set on a local filesystem where you're allowed
to own folders and files to `$BUILDER_UID:$BUILDER_UID`. Thus `/home` or other
system folders are not recommended.
export EPREFIX=/appl/prefix/2022-09
As everything in the docker image will be mounted in a different location, one
can freely move the `$LOCAL_FOLDER` around in the build machine.

# Running the build container interactively

First, let's set up the environment variables:
```sh
export LOCAL_FOLDER=/l/scibuilder_folders # This may wary based on a system where you're running
export EPREFIX=/appl/prefix/2022-09 # Location where prefix is installed in the container
export BUILDER_UID=$(id -u)
export BUILDER_OS=aalto-centos7
export SCIBUILDER_MOUNTS="-v $LOCAL_FOLDER/appl:/appl -v $LOCAL_FOLDER/spack:/spack -v $LOCAL_FOLDER/scibuilder:/scibuilder -v $LOCAL_FOLDER/cache:/cache"
```

After this, let's create the folder and get the required repositories:

```sh
mkdir -p $LOCAL_FOLDER/appl
git clone https://github.com/spack/spack.git $LOCAL_FOLDER/spack
git clone https://github.com/scifihpc/scibuilder.git $LOCAL_FOLDER/scibuilder
```

One should then use the [prefix creator](../prefix-creator/README.md) to create the prefix
to `$LOCAL_FOLDER/$EPREFIX`.

Now we can run shell inside the build image.

## Running a shell in the build image

The container takes as its arguments the `$BUILDER_UID` UID that should be
used inside of the container and the commands that should be run.

One can launch a simple terminal in the build image with:
```sh
docker run --rm -it -v $LOCAL_FOLDER/appl:/appl -v $LOCAL_FOLDER/spack:/spack -v $LOCAL_FOLDER/scibuilder:/scibuilder -v $LOCAL_FOLDER/cache:/cache aaltoscienceit/scibuilder-build-image:$BUILDER_OS $BUILDER_UID bash
```

One should be able to verify in the shell that `/appl`, `/spack`, `/scibuilder`
and `/cache` are mounted (`/cache` might be empty if build has not been run
previously).

We can clean up this command with the `$SCIBUILDER_MOUNTS`-environment variable:
```sh
docker run --rm -it $SCIBUILDER_MOUNTS aaltoscienceit/scibuilder-build-image:$BUILDER_OS $BUILDER_UID bash
```

## Running a shell in the build image with prefix activated

To activate the prefix, spack repository and the conda environment needed by the
scibuilder (which is installed in the container in `/opt/conda`) one needs to run
the `activate-scibuilder-prefix`-script in the container.

This script takes as its arguments the prefix that needs to be activated and
commands that should be run.

In this example, it is assumed that the prefix is installed in
`$LOCAL_FOLDER/appl/prefix/2022-09`. Thus inside the image the prefix will be in
`/appl/prefix/2022-09` and we can launch an interactive shell with prefix
activated with:

```sh
docker run --rm -it $SCIBUILDER_MOUNTS aaltoscienceit/scibuilder-build-image:$BUILDER_OS $BUILDER_UID activate-scibuilder-prefix $EPREFIX bash
```

## Running a shell in the build image with only spack activated

To activate the spack repository and the conda environment needed by the
scibuilder (which is installed in the container in `/opt/conda`) one needs to run
the `activate-scibuilder-spack`-script in the container.

This script takes as its arguments the commands that should be run.

For example, we can launch an interactive shell with spack activated with:
```sh
docker run --rm -it $SCIBUILDER_MOUNTS aaltoscienceit/scibuilder-build-image:$BUILDER_OS $BUILDER_UID activate-scibuilder-spack bash
```
