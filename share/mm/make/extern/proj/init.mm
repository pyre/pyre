# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter proj,$(extern)},,proj}

# # find my configuration file
proj.config := ${dir ${call extern.config,proj}}

# compiler flags
proj.flags ?=
# enable {proj} aware code
proj.defines := WITH_PROJ
# the canonical form of the include directory
proj.incpath ?= $(proj.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
proj.markers.headers ?= proj.h

# linker flags
proj.ldflags ?=
# the canonical form of the lib directory
proj.libpath ?= $(proj.dir)/lib
# its rpath
proj.rpath = $(proj.libpath)
# the names of the libraries
proj.libraries := proj

# my dependencies
proj.dependencies =


# end of file
