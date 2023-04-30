# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external dependencies
# system tools
sys.prefix := /usr
sys.lib := ${sys.prefix}/lib/x86_64-linux-gnu

# gsl
gsl.version := 2.6
gsl.dir := $(sys.prefix)
# hdf5
hdf5.version := 1.10.6
hdf5.dir := ${sys.prefix}
hdf5.parallel := openmpi
hdf5.incpath := $(hdf5.dir)/include/hdf5/$(hdf5.parallel)
hdf5.libpath := $(sys.lib)/hdf5/${hdf5.parallel}
# mpi
mpi.version := 4.1.0
mpi.flavor := openmpi
mpi.dir := ${sys.lib}/openmpi
mpi.executive := mpiexec --allow-run-as-root
# numpy
numpy.version := 1.19.5
numpy.dir := $(sys.prefix)/lib/python3/dist-packages/numpy/core
# pybind11
pybind11.version := 2.6.2
pybind11.dir = $(sys.prefix)
# python
python.version := @PYTHON_VERSION@
python.dir := $(sys.prefix)

# install locations
# this is necessary in order to override {mm} appending the build type to the install prefix
builder.dest.prefix := $(project.prefix)/
# install the python packages straight where they need to go
builder.dest.pyc := $(sys.prefix)/lib/python3/dist-packages/

# control over the build process
# set the python compiler so we don't depend on the symbolic link, which may not even be there
python3.driver := python$(python.version)


# end of file
