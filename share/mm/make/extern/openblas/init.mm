# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter openblas,$(extern)},,openblas}

# # find my configuration file
openblas.config := ${dir ${call extern.config,openblas}}

# compiler flags
openblas.flags ?=
# enable {openblas} aware code
openblas.defines := WITH_OPENBLAS
# the canonical form of the include directory
openblas.incpath ?= $(openblas.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
openblas.markers.headers ?= cblas.h

# linker flags
openblas.ldflags ?=
# the canonical form of the lib directory
openblas.libpath ?= $(openblas.dir)/lib
# its rpath
openblas.rpath = $(openblas.libpath)
# the name of the library
openblas.libraries := openblas


# end of file
