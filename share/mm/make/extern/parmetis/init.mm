# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring parmetis,$(extern)},,parmetis}

# # find my configuration file
parmetis.config := ${dir ${call extern.config,parmetis}}

# compiler flags
parmetis.flags ?=
# enable {parmetis} aware code
parmetis.defines := WITH_PARMETIS
# the canonical form of the include directory
parmetis.incpath ?= $(parmetis.dir)/include

# linker flags
parmetis.ldflags ?=
# the canonical form of the lib directory
parmetis.libpath ?= $(parmetis.dir)/lib
# the names of the libraries
parmetis.libraries := parmetis

# my dependencies
parmetis.dependencies = metis


# end of file
