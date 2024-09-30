# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring petsc,$(extern)},,petsc}

# # find my configuration file
petsc.config := ${dir ${call extern.config,petsc}}

# compiler flags
petsc.flags ?=
# enable {petsc} aware code
petsc.defines := WITH_PETSC PETSC_USE_EXTERN_CXX
# the canonical form of the include directory
petsc.incpath ?= $(petsc.dir)/include

# linker flags
petsc.ldflags ?=
# the canonical form of the lib directory
petsc.libpath ?= $(petsc.dir)/lib
# its rpath
petsc.rpath = $(petsc.libpath)
# the names of the libraries
petsc.libraries := petsc

# my dependencies
petsc.dependencies =


# end of file
