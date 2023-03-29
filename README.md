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
