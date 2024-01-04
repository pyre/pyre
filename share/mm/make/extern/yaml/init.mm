# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring yaml,$(extern)},,yaml}

# find my configuration file
yaml.config := ${dir ${call extern.config,yaml}}

# the flavor
yaml.flavor ?= -cpp
# compiler flags
yaml.flags ?=
# enable {yaml} aware code
yaml.defines ?= WITH_YAML_CPP
# the canonical form of the include directory
yaml.incpath ?= $(yaml.dir)/include

# linker flags
yaml.ldflags ?=
# the canonical form of the lib directory
yaml.libpath ?= $(yaml.dir)/lib
# the name of the library
yaml.libraries := yaml$(yaml.flavor)

# initialize the list of my dependencies
yaml.dependencies =


# end of file
