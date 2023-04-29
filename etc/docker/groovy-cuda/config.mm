# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external dependencies
# system tools
sys.prefix := /usr
sys.lib := ${sys.prefix}/lib
sys.libx86 := ${sys.lib}/x86_64-linux-gnu

# cuda
cuda.version := 10.2
cuda.dir := $(sys.prefix)
cuda.libpath := $(sys.libx86)

# fftw
fftw.version := 3.3.8
fftw.dir := $(sys.prefix)

# gsl
gsl.version := 2.5
gsl.dir := $(sys.prefix)

# libpq
libpq.version := 12.3
libpq.dir := $(sys.prefix)
libpq.libpath := $(sys.libx86)
libpq.incpath := $(sys.prefix)/include/postgresql

# mpi
mpi.version := 4.0.3
mpi.flavor := openmpi
mpi.dir := ${sys.libx86}/openmpi
mpi.executive := mpiexec --allow-run-as-root

# numpy
numpy.version := 1.17.4
numpy.dir := $(sys.prefix)/lib/python3/dist-packages/numpy/core

# pybind11
pybind11.version := 2.4.3
pybind11.dir = $(sys.prefix)

# python
python.version := @PYTHON_VERSION@
python.dir := $(sys.prefix)


# local installs
usr.prefix := /usr/local
# pyre
pyre.version := 1.9.10
pyre.dir := $(usr.prefix)
# p2
p2.version := 0.0.3
p2.dir := $(usr.prefix)


# install locations
# this is necessary in order to override {mm} appending the build type to the install prefix
builder.dest.prefix := $(project.prefix)/
# install the python packages straight where they need to go
builder.dest.pyc := $(sys.prefix)/lib/python3/dist-packages/

# control over the build process
# set the python compiler so we don't depend on the symbolic link, which may not even be there
python3.driver := python$(python.version)


# end of file
