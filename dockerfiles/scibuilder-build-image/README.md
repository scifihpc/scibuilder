# Requirements

For building and running the images it is best to use
[rootless podman](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md).

In Ubuntu 22.04, this is just:

```sh
# Install podman
sudo apt install podman
# Give user a set of UID's that the user can use to appear as root
# inside the container while being rootless outside of it
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
# Make podman aware of the change
podman system migrate
```

This will enable one to do builds in the images without ever getting root rights.

# Build the build images

Build images can be built with the following commands.

Aalto Centos 7:
```sh
podman build -t ghcr.io/scifihpc/scibuilder-build-image:aalto-centos7-v1.0.0 -f Dockerfile.aalto-centos7 .
```

HY Alma 8:
```sh
podman build -t ghcr.io/scifihpc/scibuilder-build-image:hy-alma8-v1.0.0 -f Dockerfile.hy-alma8 .
```

# Initializing the build

Before running the build we should create folders needed by the builder.
The folders are as follows:

- `$LOCAL_FOLDER` - Root folder for other folders
- `$LOCAL_FOLDER/appl` - Root folder for software.
- `$LOCAL_FOLDER/cache`- Cache repository.
- `$LOCAL_FOLDER/stage`- Stage repository.
- `$LOCAL_FOLDER/spack`- Spack repository used by the builder.
- `$LOCAL_FOLDER/scibuilder`- Scibuilder repository.

As everything in the docker image will be mounted in a different location, one
can freely move the `$LOCAL_FOLDER` around in the build machine.

When running multiple builders you will want to set up a workflow so that each
worker will get its own directories on the filesystem. This is not explained here,
as that is done by the workflow and not done manually.

Running `initialize-spack`-script in the container will download the desired
branch/tag from [spack's repository](https://github.com/spack/spack/):

```sh
# Local folder location can be changed to whatever you like
export LOCAL_FOLDER=/opt/scibuilder
# Choose build image
export BUILD_IMAGE=ghcr.io/scifihpc/scibuilder-build-image:hy-alma8-v1.0.0
# Choose spack version
export SPACK_VERSION=v0.19.1

# Create folders for the build
mkdir -p $LOCAL_FOLDER/{appl,stage,cache}
# Clone scibuilder
git clone https://github.com/scifihpc/scibuilder.git $LOCAL_FOLDER/scibuilder
# Initialize spack
podman run --rm -it -v $LOCAL_FOLDER:$LOCAL_FOLDER $BUILD_IMAGE initialize-spack $LOCAL_FOLDER/spack $SPACK_VERSION
```

You should note that the spack repository downloaded by the rootless image has
ownership rights as your user:
```sh
ls -l $LOCAL_FOLDER/spack
```

# Running the build interactively

First, let's set up environment variable for the folders:
```sh
export SCIBUILDER_MOUNTS="-v $LOCAL_FOLDER/appl:/appl -v $LOCAL_FOLDER/spack:/spack -v $LOCAL_FOLDER/scibuilder:/scibuilder -v $LOCAL_FOLDER/cache:/cache -v $LOCAL_FOLDER/stage:/stage"
```
Now we can run shell inside the build image.

## Running a shell in the build image

One can launch a simple terminal in the build image with:

We can clean up this command with the `$SCIBUILDER_MOUNTS`-environment variable:
```sh
podman run --rm -it $SCIBUILDER_MOUNTS $BUILD_IMAGE bash
```

One should be able to verify in the shell that `/appl`, `/spack`, `/scibuilder`,
`/stage` and `/cache` are mounted. Most of the folders will be empty if builds
have not been run previously).

You can verify that in the container you appear as root by running `id`.

## Running a shell in the build image with spack

To activate the spack repository and the conda environment needed by the
scibuilder (which is installed in the container in `/opt/conda`) one needs to run
the `activate-spack`-script in the container.

The script takes as its arguments commands you want to run after the activation.
For example, on can take interactive shell with activated spack with:

```sh
podman run --rm -it $SCIBUILDER_MOUNTS $BUILD_IMAGE activate-spack bash
```

One can then run `spack` to see that the spack installation is activated.

## Running an example build with scibuilder

To run a scibuilder build we want to:

1. Start in the `/scibuilder`-folder (`--workdir /scibuilder`)
2. Run scibuilder in the image after spack activation (`python -m scibuilder spack build`)
3. Run example from the `/scibuilder`-folder.

This can be brought together in the following command:
```sh
podman run --rm -it --workdir /scibuilder $SCIBUILDER_MOUNTS $BUILD_IMAGE activate-spack python -m scibuilder spack build /scibuilder/examples/build-image/spackbuilder_example.yml
```

This will run an example build.
