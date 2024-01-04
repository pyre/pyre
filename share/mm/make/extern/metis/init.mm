# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring metis,$(extern)},,metis}

# # find my configuration file
metis.config := ${dir ${call extern.config,metis}}

# compiler flags
metis.flags ?=
# enable {metis} aware code
metis.defines := WITH_METIS
# the canonical form of the include directory
metis.incpath ?= $(metis.dir)/include

# linker flags
metis.ldflags ?=
# the canonical form of the lib directory
metis.libpath ?= $(metis.dir)/lib
# the names of the libraries
metis.libraries := metis

# my dependencies
metis.dependencies =


# end of file
