# pyre

[![release](https://img.shields.io/github/v/release/pyre/pyre)](https://github.com/pyre/pyre/releases)
[![PyPI version](https://badge.fury.io/py/pyre.svg)](https://badge.fury.io/py/pyre)
[![conda version](https://img.shields.io/conda/vn/conda-forge/pyre)](https://github.com/conda-forge/pyre-feedstock)
[![mm](https://github.com/pyre/pyre/actions/workflows/mm.yaml/badge.svg)](https://github.com/pyre/pyre/actions/workflows/mm.yaml)
[![cmake](https://github.com/pyre/pyre/actions/workflows/cmake.yaml/badge.svg)](https://github.com/pyre/pyre/actions/workflows/cmake.yaml)
[![pypi source](https://github.com/pyre/pyre/actions/workflows/pypi-source.yaml/badge.svg)](https://github.com/pyre/pyre/actions/workflows/pypi-source.yaml)
[![wheels](https://github.com/pyre/pyre/actions/workflows/pypi-wheels.yaml/badge.svg)](https://github.com/pyre/pyre/actions/workflows/pypi-wheels.yaml)

A framework for building scientific applications in Python. Visit the project [homepage](http://pyre.orthologue.com) for more info

## Getting started

If you are reading this from within `pyre`, you should be able to skip to the launching
instructions at the end of this section.

Similarly, if you are lucky enough to work on a machine that is managed professionally, `pyre` may
already be installed. Please contact the system administrators for instructions about how to access
it, and skip to the end of this section.

If you are comfortable with `jupyter` notebooks, the current
[release tarball](https://github.com/aivazis/pyre/archive/refs/tags/v1.12.5.tar.gz)
contains a notebook that can walk you through the installation procedure with minimal tweaking.
It is located in `etc/mamba/pyre.ipynb`. Please report any difficulties you encounter.

The same tarball has instructions on how to build a `docker` instance with a `pyre` installation.
You will find support for many recent `ubuntu` distributions in `etc/docker`.

If none of these options work for you, read on to the next section for a walk through of how to
build `pyre` from source.

### Dependencies

The easiest way to install the `pyre` dependencies is using
[micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html) and
 `conda-forge`. The following configuration file will install everything `pyre` needs in an
environment named `pyre`. Feel free to add these packages to an existing environment, rather than
building one from scratch, although it might be easier at first if you avoid any potential conflicts
with your existing environment.

``` yaml
# -*- yaml -*-

name: pyre

channels:
  - conda-forge

dependencies:
  # python and runtime packages
  - python
  - pyyaml
  - ruamel.yaml
  # optional: external libraries
  - gsl
  - hdf5
  - libpq
  # optional: building from source
  - git
  - gcc
  - gxx
  - make
  - nodejs
  - pybind11

# end of file
```

On `macOS`, you will want to use `clang` instead of `gcc`. Make sure you activate this environment
before moving on to build `pyre` so that you use the `conda-forge` provided compilers.

It is also possible to use other package managers to install these dependencies. `pyre`
has been tested on both `ubuntu` and `macOS` using their native environments, as well as
`macports`, `homebrew`, and `spack`. Please keep in mind that most enterprise systems provide
compilers and packages that are too old to build this code, so you will have to lean on something
else to satisfy the dependencies. Further, you may have to adjust your `PATH`, `LD_LIBRARY_PATH`,
`PYTHONPATH`, and perhaps other environment variables that control access to binaries, shared
objects, and `python` packages on your machine.

### Cloning the repositories

We will need a place to clone the necessary source repositories. For the sake of concreteness, let's
pick `~/dv` as the source directory.

``` text
~> mkdir ~/dv
~> cd ~/dv
```

GitHub allows access through `ssh` or `https`, with slightly different syntax. If you already have
your `ssh` key installed on your GitHub account, you can clone the three repositories using

``` text
~/dv> git clone git@github.com:aivazis/mm
~/dv> git clone git@github.com:pyre/pyre
```

Alternatively, you can use the `https` protocol for anonymous access:

``` text
~> mkdir ~/dv
~> cd ~/dv
~/dv> git clone https://github.com/aivazis/mm
~/dv> git clone https://github.com/pyre/pyre
```

You can probably get away with installing `pyre` from `conda-forge`, but `pyre` is
currently evolving rather quickly. Being tied to a slower release cycle may delay access to
the latest features. Generally speaking, the `HEAD` of the two repositories is a safe place to
pull from, as they are thoroughly tested.

### Setting up the build system

The most involved step of the installation process is the configuration of the build system.
We will place configuration files in two locations:

``` text
~/dv> cd ~
~> mkdir -p .config/pyre
~> mkdir -p .config/mm
```

The configuration for the build system lives in `~/.config/pyre/mm.yaml`:
``` yaml
# -*- yaml -*-

# mm configuration
mm:

  # targets
  target: "opt, shared"

  # compilers
  compilers: "gcc, python/python3"

  # the following two settings get replaced with actual values by the notebook
  # the location of final products
  prefix: "{pyre.environ.CONDA_PREFIX}"
  # the installation location of the python packages, relative to {prefix}
  pycPrefix: "lib/python3.12/site-packages"
  # the location of the temporary intermediate build products
  bldroot: "{pyre.environ.HOME}/tmp/builds/mm/{pyre.environ.CONDA_DEFAULT_ENV}"

  # misc
  # the name of GNU make
  make: make
  # local makefiles
  local: Make.mmm

# end of file
```

You may need to replace `gcc` and the `python` version with whatever is available in your
environment. Incidentally, the directory `~/.config/pyre` is the home for configuration files for
all `pyre` applications, including yours, so we will be adding more files here later on.

The build system needs to know where to find headers and libraries for the `pyre` dependencies. The
package database lives in `~/.config/mm/config.mm`:

``` makefile
# -*- Makefile -*-

# external dependencies
# system tools
sys.prefix := ${CONDA_PREFIX}

# pybind11
pybind11.version := 2.11.1
pybind11.dir = $(sys.prefix)

# python: just major.minor
python.version := 3.12
python.dir := $(sys.prefix)

# pyre
pyre.version := 1.12.4
pyre.dir := $(sys.prefix)

# end of file
```

Most of the indicated package versions are there for documentation purposes, with the exception
of the `python` version that is used by `mm` to find the various directories where the interpreter
and its packages deposit files it needs.

### Building

The next step is to build `pyre`. We will invoke `mm` a few times, so you may find
it convenient to create an alias for it.

``` text
~/dv> alias mm='python3 ${HOME}/dv/mm/mm'
```

You might want to make this more permanent by also adding it to your shell startup file, e.g. your
`~/.bash_profile`.

Let's verify that everything is ok so far. Let's go to the `pyre` source directory and ask `mm` to
show details about the build. This should generate a few lines of output similar to the
following:

``` text
~/dv> cd pyre
~/dv/pyre> mm builder.info

    mm 5.0.0
    Michael Aïvázis <michael.aivazis@para-sim.com>
    copyright 1998-2025 all rights reserved

builder directory layout:
  staging layout:
           tmp = /Users/mga/tmp/builds/mm/clang/opt-shared-darwin-arm64/
  install layout:
        prefix = /Users/mga/.local/envs/pet
           bin = /Users/mga/.local/envs/pet/bin/
           doc = /Users/mga/.local/envs/pet/doc/
           inc = /Users/mga/.local/envs/pet/include/
           lib = /Users/mga/.local/envs/pet/lib/
         share = /Users/mga/.local/envs/pet/share/
           pyc = /Users/mga/.local/envs/pet/lib/python3.12/site-packages/
~/dv/pyre>
```

You may see `mm` download a `pyre` archive from `github` to bootstrap the process. This is normal,
as `mm` is itself a `pyre` application.

If anything goes wrong at this stage that cannot be resolved by retracing your steps looking for
typos, please file an [issue](https://github.com/pyre/pyre/issues) at the `pyre`
repository, and attach a log file or a screenshot to help diagnose the problem.

If everything looks ok, let's build and install `pyre`. If you are on a `linux` system, `mm` will
automatically discover the number of cores on your machine and launch a parallel build:

``` text
~/dv/pyre> mm
```

On `macOS`, it needs some help until `pyre` is built, so use something like:

``` text
~/dv/pyre> mm --slots=20
```

Don't worry if you don't have twenty cores on your machine. Most modern machines will be able to
handle this load. Feel free to up the count if you are on a machine with more cores. If all goes
well, you will have a functional `pyre` in the `site-packages` directory of your `python`
installation. Let's verify:

``` text
~/dv/pyre> python3
>>> import pyre
>>> pyre.__file__
```

Both statements should succeed, and the latter should print out the `pyre` installation location.

[comment]: <> (end of file)
