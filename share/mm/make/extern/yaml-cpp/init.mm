# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter yaml-cpp,$(extern)},,yaml-cpp}

# find my configuration file
yaml-cpp.config := ${dir ${call extern.config,yaml-cpp}}

# compiler flags
yaml-cpp.flags ?=
# enable {yaml-cpp} aware code
yaml-cpp.defines ?= WITH_YAML_CPP
# the canonical form of the include directory
yaml-cpp.incpath ?= $(yaml-cpp.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
yaml-cpp.markers.headers ?= yaml-cpp/yaml.h

# linker flags
yaml-cpp.ldflags ?=
# the canonical form of the lib directory
yaml-cpp.libpath ?= $(yaml-cpp.dir)/lib
# its rpath
yaml-cpp.rpath = $(yaml-cpp.libpath)
# the name of the library
yaml-cpp.libraries := yaml-cpp

# initialize the list of my dependencies
yaml-cpp.dependencies =


# end of file
