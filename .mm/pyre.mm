# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project meta-data
pyre.major := 1
pyre.minor := 0

# pyre builds a python package
pyre.packages := pyre.pkg journal.pkg
# a library
pyre.libraries := journal.lib pyre.lib
# a python extension
pyre.extensions := journal.ext
# and a test suite
pyre.tests := # pyre.tst.pyre pyre.tst.libpyre

# the pyre meta-data
pyre.pkg.root := packages/pyre/
pyre.pkg.stem := pyre
pyre.pkg.drivers := pyre

# the pyre meta-data
journal.pkg.root := packages/journal/
journal.pkg.stem := journal
journal.pkg.meta :=

# the journal library meta-data
journal.lib.root := lib/journal/
journal.lib.stem := journal
journal.lib.incdir := $(builder.dest.inc)pyre/journal/
journal.lib.master := journal.h
journal.lib.extern :=
journal.lib.c++.flags += $($(compiler.c++).std.c++17)

# the pyre library meta-data
pyre.lib.root := lib/pyre/
pyre.lib.stem := pyre
pyre.lib.extern := journal.lib
pyre.lib.prerequisites := journal.lib
pyre.lib.c++.flags += $($(compiler.c++).std.c++17)

# the extension meta-data
journal.ext.root := extensions/journal/
journal.ext.stem := journal
journal.ext.pkg := journal.pkg
journal.ext.wraps := journal.lib
journal.ext.extern := journal.lib python
journal.ext.prerequisites := journal.lib
journal.ext.lib.c++.flags += $($(compiler.c++).std.c++17)

# the libpyre test suite
pyre.tst.libpyre.stem := libpyre
pyre.tst.libpyre.extern := pyre.lib pyre
pyre.tst.libpyre.prerequisites := pyre.lib

# the pyre package test suite
pyre.tst.pyre.stem := pyre
pyre.tst.pyre.prerequisites := pyre.pkg pyre.ext

# end of file
