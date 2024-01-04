# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring numpy,$(extern)},,numpy}

# # find my configuration file
numpy.config := ${dir ${call extern.config,numpy}}

# compiler flags
numpy.flags ?=
# enable {numpy} aware code
numpy.defines := WITH_NUMPY
# the canonical form of the include directory
numpy.incpath ?= $(numpy.dir)/include

# linker flags
numpy.ldflags ?=
# the canonical form of the lib directory
numpy.libpath ?= $(numpy.dir)/lib
# the names of the libraries
numpy.libraries := npymath

# my dependencies
numpy.dependencies =


# end of file
