# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# add me to the pile
extern += ${if ${findstring python,$(extern)},,python}

# # find my configuration file
python.config := ${dir ${call extern.config,python}}

# the version
python.version ?= 3
# the model
python.model ?= $(empty)
# the interpreter
python.interpreter ?= python$(python.version)$(python.model)
# the configurator
python.configurator ?= $(python.interpreter)-config
# the interpreter tag, used to form pathnames
python.tag ?= $(python.interpreter)$(python.model)

# compiler flags
python.flags ?=
# enable {python} aware code
python.defines := WITH_PYTHON
# the canonical form of the include directory
python.incpath ?= $(python.dir)/include/$(python.interpreter)

# linker flags
python.ldflags ?=
# the canonical form of the lib directory
python.libpath ?= $(python.dir)/lib
# the names of the libraries
python.libraries ?= $(python.interpreter)

# now include some platform specific settings
include make/extern/python/$(platform).mm


# end of file
