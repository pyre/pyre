# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter gdal,$(extern)},,gdal}

# # find my configuration file
gdal.config := ${dir ${call extern.config,gdal}}

# compiler flags
gdal.flags ?=
# enable {gdal} aware code
gdal.defines := WITH_GDAL
# the canonical form of the include directory
gdal.incpath ?= $(gdal.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
gdal.markers.headers ?= gdal.h

# linker flags
gdal.ldflags ?=
# the canonical form of the lib directory
gdal.libpath ?= $(gdal.dir)/lib
# its rpath
gdal.rpath = $(gdal.libpath)
# the names of the libraries
gdal.libraries := gdal

# my dependencies
gdal.dependencies =


# end of file
