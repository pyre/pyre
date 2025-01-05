# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# add me to the pile
extern += ${if ${findstring summit,$(extern)},,summit}

# # find my configuration file
summit.config := ${dir ${call extern.config,summit}}

# compiler flags
summit.flags ?=
# enable {summit} aware code
summit.defines ?=
# the canonical form of the include directory
summit.incpath ?= $(summit.dir)/include

# linker flags
summit.ldflags ?=
# the canonical form of the lib directory
summit.libpath ?= $(summit.dir)/lib
# its rpath
summit.rpath = $(summit.libpath)
# the names of the libraries
summit.libraries ?= summit tetra

# my dependencies
summit.dependencies := gmsh gsl slepc petsc metis parmetis summit mpi vtk fortran


# end of file
