# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter gmsh,$(extern)},,gmsh}

# # find my configuration file
gmsh.config := ${dir ${call extern.config,gmsh}}

# compiler flags
gmsh.flags ?=
# enable {gmsh} aware code
gmsh.defines := WITH_GMSH
# the canonical form of the include directory
gmsh.incpath ?= $(gmsh.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
gmsh.markers.headers ?= gmsh.h

# linker flags
gmsh.ldflags ?=
# the canonical form of the lib directory
gmsh.libpath ?= $(gmsh.dir)/lib
# its rpath
gmsh.rpath = $(gmsh.libpath)
# the names of the libraries
gmsh.libraries := gmsh

# my dependencies
gmsh.dependencies =


# end of file
