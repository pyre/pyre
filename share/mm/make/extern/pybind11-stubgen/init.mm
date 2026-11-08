# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter pybind11-stubgen,$(extern)},,pybind11-stubgen}

# find my configuration file
pybind11-stubgen.config := ${dir ${call extern.config,pybind11-stubgen}}

# a build tool that writes the type stubs of extension modules; it runs in the interpreter
# of the build, so it contributes nothing to the compile and link lines
pybind11-stubgen.flags ?=
pybind11-stubgen.defines ?=
pybind11-stubgen.incpath ?=
pybind11-stubgen.ldflags ?=
pybind11-stubgen.libpath ?=
pybind11-stubgen.rpath ?=
pybind11-stubgen.libraries ?=

# it has no headers to look for; its module marker(s) are the modules the interpreter of the
# build must be able to import
pybind11-stubgen.markers.headers ?=
pybind11-stubgen.markers.modules ?= pybind11_stubgen

# the command line that runs it
pybind11-stubgen.driver ?= $($(compiler.python).driver) -m pybind11_stubgen

# my dependencies
pybind11-stubgen.dependencies =


# end of file
