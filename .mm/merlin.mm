# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# merlin builds a python package
merlin.packages := merlin.pkg
# some header files
merlin.libraries := merlin.mm.lib
# no python extension
merlin.extensions :=
# test suite
merlin.tests := #merlin.pkg.tests
# and files that get moved verbatim
merlin.verbatim := merlin.mm.make


# the merlin package meta-data
merlin.pkg.root := packages/merlin/
merlin.pkg.stem := merlin
merlin.pkg.ext :=
merlin.pkg.drivers := merlin mm

# the mm portinfo headers
merlin.mm.lib := lib/mm/
merlin.mm.lib.stem := mm
merlin.mm.lib.headers.extra := portinfo

# the makefile fragments
merlin.mm.make.root := share/mm/

# get the testsuites
include $(merlin.tests)


# end of file
