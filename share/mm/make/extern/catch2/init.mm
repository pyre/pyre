# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter catch2,$(extern)},,catch2}

# find my configuration file
catch2.config := ${dir ${call extern.config,catch2}}

# compiler flags
catch2.flags ?=
# enable {catch2} aware code
catch2.defines := WITH_CATCH2
# the canonical form of the include directory
catch2.incpath ?= $(catch2.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
catch2.markers.headers ?= catch2/catch_test_macros.hpp

# linker flags
catch2.ldflags ?=
# the canonical form of the lib directory
catch2.libpath ?= $(catch2.dir)/lib
# its rpath
catch2.rpath = $(catch2.libpath)
# the framework library; the {Catch2Main} entry point is added by the catch2 runner, so that
# this extern can also serve drivers that provide their own main
catch2.libraries += Catch2

# my dependencies
catch2.dependencies =


# end of file
