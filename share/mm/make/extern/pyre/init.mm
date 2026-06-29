# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter pyre,$(extern)},,pyre}

# # find my configuration file
pyre.config := ${dir ${call extern.config,pyre}}

# compiler flags
pyre.flags ?=
# enable {pyre} aware code
pyre.defines += WITH_PYRE WITH_JOURNAL
# the canonical form of the include directory
pyre.incpath ?= $(pyre.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
pyre.markers.headers ?= pyre/journal.h

# linker flags
pyre.ldflags ?=
# the canonical form of the lib directory
pyre.libpath ?= $(pyre.dir)/lib
# its rpath
pyre.rpath = $(pyre.libpath)
# the names of the libraries
pyre.libraries ?= pyre journal

# my dependencies
pyre.dependencies =


# end of file
