# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter libpq,$(extern)},,libpq}

# # find my configuration file
libpq.config := ${dir ${call extern.config,libpq}}

# compiler flags
libpq.flags ?=
# enable {libpq} aware code
libpq.defines := WITH_LIBPQ
# the canonical form of the include directory
libpq.incpath ?= $(libpq.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
libpq.markers.headers ?= libpq-fe.h

# linker flags
libpq.ldflags ?=
# the canonical form of the lib directory
libpq.libpath ?= $(libpq.dir)/lib
# its rpath
libpq.rpath = $(libpq.libpath)
# the names of the libraries
libpq.libraries := pq

# my dependencies
libpq.dependencies =


# end of file
