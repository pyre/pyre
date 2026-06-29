# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter cantera,$(extern)},,cantera}

# # find my configuration file
cantera.config := ${dir ${call extern.config,cantera}}

# compiler flags
cantera.flags ?=
# enable {cantera} aware code
cantera.defines ?= WITH_CANTERA
# the canonical form of the include directory
cantera.incpath ?= $(cantera.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
cantera.markers.headers ?= cantera/base/ct_defs.h

# linker flags
cantera.ldflags ?=
# the canonical form of the lib directory
cantera.libpath ?= $(cantera.dir)/lib
# its rpath
cantera.rpath = $(cantera.libpath)
# the names of the libraries
cantera.libraries ?= cantera cantera_fortran

# my dependencies
cantera.dependencies := eigen sundials openblas yaml-cpp fmt fortran


# end of file
