# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# pyre builds a python package
pyre.packages := pyre.pkg
# libraries
pyre.libraries := pyre.lib
# the mandatory extensions
pyre.extensions := pyre.ext

# and test suites
pyre.tests := pyre.python.tests pyre.pkg.tests pyre.lib.tests pyre.ext.tests sqlite.pkg.tests

# we also some files that get moved verbatim
pyre.verbatim := pyre.templates

# the bootstrap bundle
pyre.boot.packages := pyre.pkg journal.pkg merlin.pkg survey.pkg
# the bootstrap zip file entry point
pyre.boot.main := etc/boot/main.py


# predicates that check the c++ standard in use
# these are low resolution tests and may not be good enough
pyre.c++20 = \
  ${findstring \
    $($(compiler.c++).std.c++20), \
    $(pyre.lib.c++.flags) \
  }


# the pyre package meta-data
pyre.pkg.root := packages/pyre/
pyre.pkg.stem := pyre
pyre.pkg.drivers := pyre pyre-config smith.pyre
pyre.pkg.config := pyre
pyre.pkg.ext := extensions/


# the pyre library meta-data
pyre.lib.root := lib/pyre/
pyre.lib.stem := pyre
pyre.lib.prerequisites += chroma.lib journal.lib
pyre.lib.c++.defines += PYRE_CORE
pyre.lib.c++.flags += -Wall $($(compiler.c++).std.c++17)

# additional macros that enable features sensitive to the c++ standard version
pyre.lib.c++.defines += \
  ${if $(pyre.c++20),\
    HAVE_COMPACT_PACKINGS WITH_CXX20 \
  }

# external dependencies
pyre.lib.extern := journal.lib


# the pyre extensions
# {libpyre} bindings
pyre.ext.root := extensions/pyre/
pyre.ext.stem := pyre
pyre.ext.pkg := pyre.pkg
pyre.ext.wraps := pyre.lib
pyre.ext.capsule :=
pyre.ext.extern := journal.lib pybind11 python
pyre.ext.lib.c++.flags += $(pyre.lib.c++.flags)
pyre.ext.lib.c++.defines += $(pyre.lib.c++.defines)
pyre.ext.lib.prerequisites += chroma.lib journal.lib # pyre.lib is added automatically


# the templates
pyre.templates.root := templates/


# get the docker image definitions
include pyre-docker.mm

# get the test suites
include $(pyre.tests)


# end of file
