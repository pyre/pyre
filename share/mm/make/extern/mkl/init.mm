# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter mkl,$(extern)},,mkl}

# find my configuration file
mkl.config := ${dir ${call extern.config,mkl}}

# compiler flags
mkl.flags ?=
# enable {mkl} aware code
mkl.defines := WITH_MKL
# the canonical form of the include directory
mkl.incpath ?= $(mkl.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
mkl.markers.headers ?= mkl.h

# linker flags
mkl.ldflags ?=
# the canonical form of the lib directory
mkl.libpath ?= $(mkl.dir)/lib
# its rpath
mkl.rpath = $(mkl.libpath)
# the set of mkl libraries to link against
mkl.libraries ?=


# end of file
