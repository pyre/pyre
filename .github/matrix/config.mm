# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved

# external dependencies
# system tools
sys.prefix := /usr
sys.lib := ${sys.prefix}/lib
sys.libx86 := ${sys.lib}/x86_64-linux-gnu

# gsl
gsl.version := 2.5
gsl.dir := $(sys.prefix)
# mpi
mpi.version := 4.0.3
mpi.flavor := openmpi
mpi.dir := ${sys.libx86}/openmpi
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
clang.driver := clang-$(suiteVesion)
clang++.driver := clang++-$(suiteVesion)
# the gcc drivers
gcc.driver := gcc-$(suiteVesion)
g++.driver := g++-$(suiteVesion)
# the python driver
python3.driver := python$(python.version)

# end of file
