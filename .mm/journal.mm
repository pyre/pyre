# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# project meta-data
journal.major := $(repo.major)
journal.minor := $(repo.minor)
journal.micro := $(repo.micro)
journal.revision := $(repo.revision)


# journal builds a python package
journal.packages := journal.pkg
# a library
journal.libraries := journal.lib
# a python extension
journal.extensions := journal.ext
# and test suites
journal.tests := journal.pkg.tests journal.lib.tests


# the journal package meta-data
journal.pkg.root := packages/journal/
journal.pkg.stem := journal
journal.pkg.ext :=

# the journal library meta-data
journal.lib.root := lib/journal/
journal.lib.stem := journal
journal.lib.incdir := $(builder.dest.inc)pyre/journal/
journal.lib.master := journal.h
journal.lib.extern :=
journal.lib.c++.defines += PYRE_CORE
journal.lib.c++.flags += $($(compiler.c++).std.c++17)


# the journal extension meta-data
journal.ext.root := extensions/journal/
journal.ext.stem := journal
journal.ext.pkg := journal.pkg
journal.ext.wraps := journal.lib
journal.ext.capsule :=
journal.ext.extern := journal.lib python
journal.ext.lib.c++.defines += PYRE_CORE
journal.ext.lib.c++.flags += $($(compiler.c++).std.c++17)


# get the testsuites
include journal.pkg.tests journal.lib.tests


# end of file
