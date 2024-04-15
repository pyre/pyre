# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring vtk,$(extern)},,vtk}

# # find my configuration file
vtk.config := ${dir ${call extern.config,vtk}}

# users set this variable to communicate which libraries they want
vtk.required ?=

# compiler flags
vtk.flags ?=
# enable {vtk} aware code
vtk.defines := WITH_VTK
# the canonical form of the include directory
vtk.incpath ?= $(vtk.dir)/include/vtk-$(vtk.version)

# linker flags
vtk.ldflags ?=
# the canonical form of the lib directory
vtk.libpath ?= $(vtk.dir)/lib
# its rpath
vtk.rpath = $(vtk.libpath)
# the way library names are formed is version dependent; we support 6.x and higher
vtk.libraries := \
    ${foreach \
        requirement, \
        $(vtk.required), \
        vtk$(requirement)-$(vtk.version) \
    }


# end of file
