# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring cantera,$(extern)},,cantera}

# # find my configuration file
cantera.config := ${dir ${call extern.config,cantera}}

# compiler flags
cantera.flags ?=
# enable {cantera} aware code
cantera.defines ?= WITH_CANTERA
# the canonical form of the include directory
cantera.incpath ?= $(cantera.dir)/include

# linker flags
cantera.ldflags ?=
# the canonical form of the lib directory
cantera.libpath ?= $(cantera.dir)/lib
# its rpath
cantera.rpath = $(cantera.libpath)
# the names of the libraries
cantera.libraries ?= cantera cantera_fortran

# my dependencies
cantera.dependencies := eigen sundials openblas yaml fmt fortran


# end of file
