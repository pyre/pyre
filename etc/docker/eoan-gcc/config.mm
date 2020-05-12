# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# external dependencies
# system tools
sys.prefix := /usr
sys.lib := ${sys.prefix}/lib
sys.libx86 := ${sys.lib}/x86_64-linux-gnu

# gsl
gsl.version := 2.5
gsl.dir := $(sys.prefix)
# mpi
mpi.version := 3.1.3
mpi.flavor := openmpi
mpi.dir := ${sys.libx86}/openmpi
mpi.executive := mpiexec --allow-run-as-root
# numpy
numpy.version := 1.16.2
numpy.dir := $(sys.prefix)/lib/python3/dist-packages/numpy/core
# pybind11
pybind11.version := 2.3.0
pybind11.dir = $(sys.prefix)
# python
python.version := @PYTHON_VERSION@
python.model := @PYTHON_MODEL@
python.dir := $(sys.prefix)
python.incdir := $(python.dir)/include/python$(python.version)
python.libdir := $(python.dir)/lib/python$(python.version)

# install locations
# this is necessary in order to override {mm} appending the build type to the install prefix
builder.dest.prefix := $(project.prefix)/
# install the pyton packages straight where they need to go
builder.dest.pyc := $(sys.prefix)/lib/python3/dist-packages/

# control over the build process
# set the python compiler so we don't depend on the symbolic link, which may not even be there
compiler.python := python$(python.version)


# end of file
