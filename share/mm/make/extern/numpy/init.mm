# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter numpy,$(extern)},,numpy}

# # find my configuration file
numpy.config := ${dir ${call extern.config,numpy}}

# compiler flags
numpy.flags ?=
# enable {numpy} aware code
numpy.defines := WITH_NUMPY
# the canonical form of the include directory
numpy.incpath ?= $(numpy.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
numpy.markers.headers ?= numpy/arrayobject.h

# linker flags
numpy.ldflags ?=
# the canonical form of the lib directory
numpy.libpath ?= $(numpy.dir)/lib
# its rpath
numpy.rpath = $(numpy.libpath)
# the names of the libraries
numpy.libraries := npymath

# my dependencies
numpy.dependencies =


# end of file
