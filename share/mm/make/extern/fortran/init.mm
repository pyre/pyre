# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring fortran,$(extern)},,fortran}

# # find my configuration file
fortran.config := ${dir ${call extern.config,fortran}}

# compiler flags
fortran.flags ?= $($(compiler.fortran).mixed.flags)
# enable {fortran} aware code
fortran.defines ?= $($(compiler.fortran).mixed.defines)
# the canonical form of the include directory
fortran.incpath ?= $($(compiler.fortran).mixed.incpath)

# linker flags
fortran.ldflags ?= $($(compiler.fortran).mixed.ldflags)
# the canonical form of the lib directory
fortran.libpath ?= $($(compiler.fortran).mixed.libpath)
# its rpath
fortran.rpath = $(fortran.libpath)
# the names of the libraries
fortran.libraries ?= $($(compiler.fortran).mixed.libraries)

# my dependencies
fortran.dependencies =


# end of file
