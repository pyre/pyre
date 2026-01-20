# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${findstring cspice,$(extern)},,cspice}

# # find my configuration file
cspice.config := ${dir ${call extern.config,cspice}}

# compiler flags
cspice.flags ?=
# enable {cspice} aware code
cspice.defines := WITH_CSPICE
# the canonical form of the include directory
cspice.incpath ?= $(cspice.dir)/include

# linker flags
cspice.ldflags ?=
# the canonical form of the lib directory
cspice.libpath ?= $(cspice.dir)/lib
# its rpath
cspice.rpath = $(cspice.libpath)
# the names of the libraries
cspice.libraries := cspice

# my dependencies
cspice.dependencies =


# end of file
