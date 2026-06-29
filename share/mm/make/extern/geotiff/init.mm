# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter geotiff,$(extern)},,geotiff}

# # find my configuration file
geotiff.config := ${dir ${call extern.config,geotiff}}

# compiler flags
geotiff.flags ?=
# enable {geotiff} aware code
geotiff.defines := WITH_GEOTIFF
# the canonical form of the include directory
geotiff.incpath ?= $(geotiff.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
geotiff.markers.headers ?= geotiff.h

# linker flags
geotiff.ldflags ?=
# the canonical form of the lib directory
geotiff.libpath ?= $(geotiff.dir)/lib
# its rpath
geotiff.rpath = $(geotiff.libpath)
# the names of the libraries
geotiff.libraries := geotiff tiff

# my dependencies
geotiff.dependencies = tiff


# end of file
