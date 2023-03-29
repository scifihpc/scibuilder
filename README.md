# Scibuilder

Scibuilder is a tool for helping with automated builds 

## Installation

Scibuilder is a Python module and it needs an environment with various packages.

We recommend using `mamba` for faster installation.
[Mambaforge](https://github.com/conda-forge/miniforge#install) is an excellent way
of getting `mamba`.

Creating environment:

```sh
mamba env create --file environment.yml
source activate scibuilder
```

## Running scibuilder example

### Spack

This example build works on Ubuntu 22.04. It installs cmake as an example.

```sh
git clone https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
python -m scibuilder spack build examples/without-image/spackbuilder_example.yml
```

### Mamba

This example build will work on any linux system. It creates two conda environments:
one with gpu-enabled packgages and one without.

```sh
python -m scibuilder mamba build examples/without-image/mambabuilder_example.yml
```

## scibuilder-build-image

Scibuilder can be run in a docker/podman images.

See image [README.md](dockerfiles/scibuilder-build-image/README.md) for more information.

## Configuring builds

### Spack

Spack builds are configured by creating a YAML-file that describes what environments we
want to build and the compilers we want to use for building them.

Let's look at [examples/without-image/spackbuilder_example.yml](examples/without-image/spackbuilder_example.yml):

```yml
environments:
  - name: spack_example
    tags:
      - spack
      - main
    environment_file: examples/without-image/spack_example_ubuntu22.04/spack.yaml
    system_compiler: "gcc@11.3.0"
    compilers:
      - "gcc@11.3.0"
```

The list `environments` consist of multiple independent build with the following
attributes:

- `name` - Name of the environment
- `tags` - List of arbitrary tags that can be used to limit the builder to only these
  builds via the `--tags=TAGS`-parameter.
- `environmnet_file` - A spack [environement file](https://spack.readthedocs.io/en/latest/environments.html)
  that contains information on what packages we want to install and where we want to install them.
- `system_compiler` - A compiler present in the system that the builder will try to locate for
  spack to use as an initial compiler.
- `compilers`: List of compilers that spack will try to locate and build with the system compiler
  before building the environment in full.
