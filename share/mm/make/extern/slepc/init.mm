# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring slepc,$(extern)},,slepc}

# # find my configuration file
slepc.config := ${dir ${call extern.config,slepc}}

# compiler flags
slepc.flags ?=
# enable {slepc} aware code
slepc.defines := WITH_SLEPC SLEPC_USE_EXTERN_CXX
# the canonical form of the include directory
slepc.incpath ?= $(slepc.dir)/include

# linker flags
slepc.ldflags ?=
# the canonical form of the lib directory
slepc.libpath ?= $(slepc.dir)/lib
# the names of the libraries
slepc.libraries := slepc

# my dependencies
slepc.dependencies = petsc


# end of file
