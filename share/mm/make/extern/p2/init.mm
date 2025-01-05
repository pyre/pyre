# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# add me to the pile
extern += ${if ${findstring p2,$(extern)},,p2}

# # find my configuration file
p2.config := ${dir ${call extern.config,p2}}

# compiler flags
p2.flags ?=
# enable {p2} aware code
p2.defines += WITH_PYRE WITH_JOURNAL
# the canonical form of the include directory
p2.incpath ?= $(p2.dir)/include

# linker flags
p2.ldflags ?=
# the canonical form of the lib directory
p2.libpath ?= $(p2.dir)/lib
# its rpath
p2.rpath = $(p2.libpath)
# the names of the libraries
p2.libraries ?= # p2

# my dependencies
p2.dependencies =


# end of file
