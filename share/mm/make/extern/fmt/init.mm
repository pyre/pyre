# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter fmt,$(extern)},,fmt}

# # find my configuration file
fmt.config := ${dir ${call extern.config,fmt}}

# compiler flags
fmt.flags ?=
# enable {fmt} aware code
fmt.defines ?= WITH_FMT
# the canonical form of the include directory
fmt.incpath ?= $(fmt.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
fmt.markers.headers ?= fmt/format.h

# linker flags
fmt.ldflags ?=
# the canonical form of the lib directory
fmt.libpath ?= $(fmt.dir)/lib
# its rpath
fmt.rpath = $(fmt.libpath)
# the names of the libraries
fmt.libraries ?=  fmt

# my dependencies
fmt.dependencies :=


# end of file
