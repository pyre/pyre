# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring cgal,$(extern)},,cgal}

# find my configuration file
cgal.config := ${dir ${call extern.config,cgal}}

# compiler flags
cgal.flags ?=
# enable {cgal} aware code
cgal.defines := WITH_CGAL
# the canonical form of the include directory
cgal.incpath ?= $(cgal.dir)/include

# linker flags
cgal.ldflags ?=
# the canonical form of the lib directory
cgal.libpath ?=
# the name of the library
cgal.libraries :=

# initialize the list of my dependencies
cgal.dependencies =


# end of file
