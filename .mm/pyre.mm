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
pyre.packages := pyre.pkg
# a library
pyre.libraries := journal.lib pyre.lib
# a python extension
pyre.extensions := # pyre.ext
# and a test suite
pyre.tests := # pyre.tst.pyre pyre.tst.libpyre

# the package meta-data
pyre.pkg.root := packages/pyre/
pyre.pkg.stem := pyre
pyre.pkg.drivers := pyre

# the journal library meta-data
journal.lib.root := lib/journal/
journal.lib.stem := journal
journal.lib.incdir := $(builder.dest.inc)pyre/journal/
journal.lib.master := journal.h
journal.lib.extern :=

# the pyre library meta-data
pyre.lib.root := lib/pyre/
pyre.lib.stem := pyre
pyre.lib.extern := journal.lib
pyre.lib.prerequisites := journal.lib

# the extension meta-data
pyre.ext.stem := pyre
pyre.ext.pkg := pyre.pkg
pyre.ext.wraps := pyre.lib
pyre.ext.extern := pyre.lib python

# the libpyre test suite
pyre.tst.libpyre.stem := libpyre
pyre.tst.libpyre.extern := pyre.lib pyre
pyre.tst.libpyre.prerequisites := pyre.lib

# the pyre package test suite
pyre.tst.pyre.stem := pyre
pyre.tst.pyre.prerequisites := pyre.pkg pyre.ext


# testsuite

# the foo/sanity.py test cases
pyre.tst.pyre.foo.sanity.cases := foo.sanity.help foo.sanity.friend
# command lines
foo.sanity.help := --help
foo.sanity.friend := --friend=ally

# end of file
