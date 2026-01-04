# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${findstring pybind11,$(extern)},,pybind11}

# # find my configuration file
pybind11.config := ${dir ${call extern.config,pybind11}}

# compiler flags
pybind11.flags ?=
# enable {pybind11} aware code
pybind11.defines := WITH_PYBIND11
# the canonical form of the include directory
pybind11.incpath ?= $(pybind11.dir)/include

# linker flags
pybind11.ldflags ?=
# the canonical form of the lib directory
pybind11.libpath ?=
# its rpath
pybind11.rpath = $(pybind11.libpath)
# the names of the libraries
pybind11.libraries :=

# my dependencies
pybind11.dependencies =


# end of file
