# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter gtest,$(extern)},,gtest}

# # find my configuration file
gtest.config := ${dir ${call extern.config,gtest}}

# compiler flags
gtest.flags ?=
# enable {gtest} aware code
gtest.defines := WITH_GTEST
# the canonical form of the include directory
gtest.incpath ?= $(gtest.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
gtest.markers.headers ?= gtest/gtest.h

# linker flags
gtest.ldflags ?=
# the canonical form of the lib directory
gtest.libpath ?= $(gtest.dir)/lib
# its rpath
gtest.rpath = $(gtest.libpath)
# the names of the libraries
gtest.libraries += gtest pthread

# my dependencies
gtest.dependencies =


# end of file
