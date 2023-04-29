# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# journal builds a python package
journal.packages := journal.pkg
# a library
journal.libraries := journal.lib
# a python extension
journal.extensions := journal.ext
# and test suites
journal.tests := journal.pkg.tests journal.lib.tests journal.ext.tests journal.api.tests


# the journal package meta-data
journal.pkg.root := packages/journal/
journal.pkg.stem := journal
journal.pkg.prerequisites := pyre.pkg

# the journal library meta-data
# the stem; used to derive the location and name of the library; it should be deducible from
# the name of the project, but just in case...
journal.lib.stem := journal
# the destination include directory
journal.lib.incdir := $(builder.dest.inc)pyre/journal/
# the main api header file; it is deposited one level above the rest
journal.lib.gateway := journal.h
# compiler control
journal.lib.c++.defines += PYRE_CORE
journal.lib.c++.flags += $($(compiler.c++).std.c++17)


# the journal extension meta-data
# the stem; used to derive the location and name of the extension; it should be deducible from
# the name of the project, but just in case...
journal.ext.stem := journal
# the location of the source relative to the project home diretcory
journal.ext.root := extensions/journal/
journal.ext.capsule :=
journal.ext.wraps := journal.lib
journal.ext.extern := pybind11 python
# compiler control
journal.ext.lib.c++.defines += PYRE_CORE
journal.ext.lib.c++.flags += $($(compiler.c++).std.c++17)


# get the testsuites
include $(journal.tests)


# end of file
