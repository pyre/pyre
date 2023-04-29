# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# check availability
mpi.available := ${findstring mpi,$(extern.available)}

# if {mpi} is available
ifeq ($(mpi.available), mpi)


# mpi builds a python package
pyre-mpi.packages := pyre-mpi.pkg
# a library
pyre-mpi.libraries := pyre-mpi.lib
# a python extension
pyre-mpi.extensions := pyre-mpi.ext
# and test suites
pyre-mpi.tests := pyre-mpi.pkg.tests pyre-mpi.lib.tests


# the mpi package meta-data
pyre-mpi.pkg.root := packages/mpi/
pyre-mpi.pkg.stem := mpi
pyre-mpi.pkg.ext :=

# the mpi library meta-data
pyre-mpi.lib.root := lib/mpi/
pyre-mpi.lib.stem := mpi
pyre-mpi.lib.incdir := $(builder.dest.inc)pyre/mpi/
pyre-mpi.lib.gateway := mpi.h
pyre-mpi.lib.prerequisites := journal.lib
pyre-mpi.lib.extern := journal.lib mpi
pyre-mpi.lib.c++.flags += $($(compiler.c++).std.c++17)

# the mpi extension meta-data
pyre-mpi.ext.root := extensions/mpi/
pyre-mpi.ext.stem := mpi
pyre-mpi.ext.pkg := pyre-mpi.pkg
pyre-mpi.ext.wraps := pyre-mpi.lib
pyre-mpi.ext.capsule.destination := pyre/mpi/
pyre-mpi.ext.lib.prerequisites := pyre-mpi.lib pyre.lib
pyre-mpi.ext.extern := pyre.lib journal.lib mpi python
pyre-mpi.ext.lib.c++.flags += $($(compiler.c++).std.c++17)


# get the testsuites
include pyre-mpi.pkg.tests pyre-mpi.lib.tests


endif


# end of file
