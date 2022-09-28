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

# Running the build container interactively

The container takes as its argument the `$BUILDER_UID` UID that should be used inside of the container.

One can launch the build image with Gentoo prefix mounted from `$EPREFIX` with the following commands:
```sh
EPREFIX=/appl/prefix/2022-09
BUILDER_UID=$(id -u)
BUILDER_OS=aalto-centos7
docker run -v /tmp/$EPREFIX:$EPREFIX --rm -it aaltoscienceit/scibuilder-build-image:$BUILDER_OS $BUILDER_UID
```

This will launch an interactive shell within the image.
One can then start the prefix with
```sh
EPREFIX=/appl/prefix/2022-09
source $EPREFIX/startprefix
```

After this one can run spack etc. with respect to the prefix.
One should preferable mount the spack from outside of the container into to the container.
