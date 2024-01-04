# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring openblas,$(extern)},,openblas}

# # find my configuration file
openblas.config := ${dir ${call extern.config,openblas}}

# compiler flags
openblas.flags ?=
# enable {openblas} aware code
openblas.defines := WITH_OPENBLAS
# the canonical form of the include directory
openblas.incpath ?= $(openblas.dir)/include

# linker flags
openblas.ldflags ?=
# the canonical form of the lib directory
openblas.libpath ?= $(openblas.dir)/lib
# the name of the library
openblas.libraries := openblas


# end of file
