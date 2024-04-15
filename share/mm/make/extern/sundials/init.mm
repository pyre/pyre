# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring sundials,$(extern)},,sundials}

# # find my configuration file
sundials.config := ${dir ${call extern.config,sundials}}

# compiler flags
sundials.flags ?=
# enable {sundials} aware code
sundials.defines ?= WITH_SUNDIALS
# the canonical form of the include directory
sundials.incpath ?= $(sundials.dir)/include

# linker flags
sundials.ldflags ?=
# the canonical form of the lib directory
sundials.libpath ?= $(sundials.dir)/lib
# its rpath
sundials.rpath = $(sundials.libpath)
# the names of the libraries
sundials.libraries ?= sundials_cvodes sundials_ida sundials_nvecserial sundials_sunlinsoldense sundials_sunlinsolband

# my dependencies
sundials.dependencies :=


# end of file
