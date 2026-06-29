# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter petsc,$(extern)},,petsc}

# # find my configuration file
petsc.config := ${dir ${call extern.config,petsc}}

# compiler flags
petsc.flags ?=
# enable {petsc} aware code
petsc.defines := WITH_PETSC PETSC_USE_EXTERN_CXX
# the canonical form of the include directory
petsc.incpath ?= $(petsc.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
petsc.markers.headers ?= petscversion.h

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
