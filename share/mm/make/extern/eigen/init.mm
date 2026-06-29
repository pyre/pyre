# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter eigen,$(extern)},,eigen}

# # find my configuration file
eigen.config := ${dir ${call extern.config,eigen}}

# flags
eigen.flags ?=
# enable {eigen} aware code
eigen.defines := WITH_EIGEN3
# the canonical form of the include directory
eigen.incpath ?= $(eigen.dir)/include/eigen3
# header marker(s): files that must resolve on {incpath}; absence proves breakage
eigen.markers.headers ?= Eigen/Core

# linker flags
eigen.ldflags ?=
# the canonical form of the lib directory
eigen.libpath ?=
# its rpath
eigen.rpath = $(eigen.libpath)
# the names of the libraries
eigen.libraries :=

# my dependencies
eigen.dependencies =


# end of file
