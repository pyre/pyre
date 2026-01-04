# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# show me
# ${info -- fmm3d.init}

# add me to the pile
extern += ${if ${findstring fmm3d,$(extern)},,fmm3d}

# # find my configuration file
fmm3d.config := ${dir ${call extern.config,fmm3d}}

# compiler flags
fmm3d.flags ?=
# enable {cantera} aware code
fmm3d.defines ?= WITH_FMM3D
# the canonical form of the include directory
fmm3d.incpath ?= $(fmm3d.dir)/include

# linker flags
fmm3d.ldflags ?= std=legacy
# the canonical form of the lib directory
fmm3d.libpath ?= $(fmm3d.dir)/lib
# its rpath
fmm3d.rpath = $(fmm3d.libpath)
# the names of the libraries
fmm3d.libraries ?= fmm3d

# my dependencies
fmm3d.dependencies := fortran

# show me
# ${info -- done with fmm3d.init}

# end of file
