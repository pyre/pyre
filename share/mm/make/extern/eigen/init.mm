# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# add me to the pile
extern += ${if ${findstring eigen,$(extern)},,eigen}

# # find my configuration file
eigen.config := ${dir ${call extern.config,eigen}}

# flags
eigen.flags ?=
# enable {eigen} aware code
eigen.defines := WITH_EIGEN3
# the canonical form of the include directory
eigen.incpath ?= $(eigen.dir)/include/eigen3

# linker flags
eigen.ldflags ?=
# the canonical form of the lib directory
eigen.libpath ?=
# its rpath
eigen.rpath = $(eigen.libpath)
# the names of the libraries
eigen.libraries :=

# my dependencies
eigen.dependencies =


# end of file
