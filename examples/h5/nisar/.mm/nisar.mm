# -*- makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# nisar consists of a python package
nisar.packages := nisar.pkg
# and some tests
nisar.tests := nisar.pkg.tests


# load the packages
include $(nisar.packages)
# and the test suites
include $(nisar.tests)


# end of file
