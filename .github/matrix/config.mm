# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# external dependencies
# system tools
sys.prefix := /usr
sys.lib := ${sys.prefix}/lib/x86_64-linux-gnu

# gsl
gsl.version := 2.5
gsl.dir := $(sys.prefix)

# hdf5
hdf5.version := 1.10.6
hdf5.dir := ${sys.prefix}
hdf5.parallel := serial
hdf5.incpath := $(hdf5.dir)/include/hdf5/$(hdf5.parallel)
hdf5.libpath := $(sys.lib)/hdf5/${hdf5.parallel}

# mpi
mpi.version := 4.0.3
mpi.flavor := openmpi
mpi.dir := ${sys.lib}/$(mpi.flavor)
mpi.executive := mpiexec

# python
python.version := $(pythonVersion)
python.dir := $(pythonLocation)

# numpy
numpy.version := 1.21.1
numpy.dir := $(python.dir)/lib/python$(python.version)/site-packages/numpy/core

# pybind11
pybind11.version := 2.7.0
pybind11.dir := $(python.dir)/lib/python$(python.version)/site-packages/pybind11

# control over the build process
# the clang drivers
clang.driver := clang-$(suiteVersion)
clang++.driver := clang++-$(suiteVersion)
# the gcc drivers
gcc.driver := gcc-$(suiteVersion)
g++.driver := g++-$(suiteVersion)
# the python driver
python3.driver := python$(python.version)

# end of file
