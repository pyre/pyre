# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring cuda,$(extern)},,cuda}

# find my configuration file
cuda.config := ${dir ${call extern.config,cuda}}

# compiler flags
cuda.flags ?=
# enable {cuda} aware code
cuda.defines += WITH_CUDA
# the canonical form of the include directory
cuda.incpath ?= $(cuda.dir)/include

# linker flags
cuda.ldflags ?=
# the canonical form of the lib directory
cuda.libpath ?= $(cuda.dir)/lib64
# the set of cuda libraries to link against
cuda.libraries ?=


# end of file
