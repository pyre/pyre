# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# external dependencies
# system tools
sys.prefix := /usr
# gsl
gsl.version := 2.5
gsl.dir := $(sys.prefix)
# numpy
numpy.version := 1.17.4
numpy.dir := $(sys.prefix)/lib/python3/dist-packages/numpy/core
# pybind11
pybind11.version := 2.4.3
pybind11.dir = $(sys.prefix)
# python
python.version := @PYTHON_VERSION@
python.dir := $(sys.prefix)
python.incdir := $(python.dir)/include/python$(python.version)
python.libdir := $(python.dir)/lib/python$(python.version)


# install locations
# this is necessary in order to override {mm} appending the build type to the install prefix
builder.dest.prefix := $(project.prefix)/


# control over the build process
# set the python compiler so we don't depend on the symbolic link, which may not even be there
compiler.python := python$(python.version)


# end of file
