# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter vtk,$(extern)},,vtk}

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
# header marker(s): files that must resolve on {incpath}; absence proves breakage
vtk.markers.headers ?= vtkVersion.h

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
# {libraries} is built from the user's {vtk.required} module list; with none nominated it comes out
# empty and the link drops every vtk symbol, so declare it required and hint at the fix
vtk.markers.required ?= libraries
vtk.markers.required.hint ?= "(set vtk.required to the vtk modules you need, e.g. CommonCore IOXML)"


# end of file
