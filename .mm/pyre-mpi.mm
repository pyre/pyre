# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# check availability
mpi.available := ${findstring mpi,$(extern.available)}


# the pure-python {mpi} package ships unconditionally: it degrades to a trivial single-process
# communicator when the {libmpi} bindings are absent, so code written against it runs anywhere
pyre-mpi.packages := pyre-mpi.pkg

# the mpi package meta-data
pyre-mpi.pkg.root := packages/mpi/
pyre-mpi.pkg.stem := mpi
pyre-mpi.pkg.ext :=


# the library and the extension that wraps it need the actual mpi runtime
ifeq ($(mpi.available), mpi)


# a library
pyre-mpi.libraries := pyre-mpi.lib
# a python extension
pyre-mpi.extensions := pyre-mpi.ext
# and test suites
pyre-mpi.tests := pyre-mpi.pkg.tests pyre-mpi.ext.tests pyre-mpi.lib.tests


# the mpi library meta-data
pyre-mpi.lib.root := lib/mpi/
pyre-mpi.lib.stem := mpi
pyre-mpi.lib.incdir := $(builder.dest.inc)pyre/mpi/
pyre-mpi.lib.gateway := mpi.h
pyre-mpi.lib.prerequisites := journal.lib
pyre-mpi.lib.extern := journal.lib mpi
pyre-mpi.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-mpi.lib.c++.defines += $(pyre.lib.c++.defines)

# the mpi extension meta-data
pyre-mpi.ext.root := extensions/mpi/
# the module is {libmpi}, so that it does not shadow the {mpi} package that hosts it, and so
# that it reads like its siblings {libpyre} and {libh5}
pyre-mpi.ext.stem := libmpi
pyre-mpi.ext.pkg := pyre-mpi.pkg
pyre-mpi.ext.wraps := pyre-mpi.lib
# the bindings hand back real classes now, so there are no capsule headers to publish
pyre-mpi.ext.capsule :=
pyre-mpi.ext.lib.prerequisites := pyre-mpi.lib pyre.lib
pyre-mpi.ext.extern := pyre.lib journal.lib mpi pybind11 python
pyre-mpi.ext.lib.c++.flags += $(pyre-mpi.lib.c++.flags)
pyre-mpi.ext.lib.c++.defines += $(pyre-mpi.lib.c++.defines)


# get the testsuites
include pyre-mpi.pkg.tests pyre-mpi.ext.tests pyre-mpi.lib.tests


endif


# end of file
