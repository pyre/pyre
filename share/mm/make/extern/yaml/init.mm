# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter yaml,$(extern)},,yaml}

# find my configuration file
yaml.config := ${dir ${call extern.config,yaml}}

# compiler flags
yaml.flags ?=
# enable {yaml} aware code
yaml.defines ?= WITH_LIBYAML
# the canonical form of the include directory
yaml.incpath ?= $(yaml.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
yaml.markers.headers ?= yaml.h

# linker flags
yaml.ldflags ?=
# the canonical form of the lib directory
yaml.libpath ?= $(yaml.dir)/lib
# its rpath
yaml.rpath = $(yaml.libpath)
# the name of the library
yaml.libraries := yaml

# initialize the list of my dependencies
yaml.dependencies =


# end of file
