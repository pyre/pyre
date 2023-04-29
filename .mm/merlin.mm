# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# merlin builds a python package
merlin.packages := merlin.pkg
# no library
merlin.libraries :=
# no python extension
merlin.extensions :=
# test suite
merlin.tests := #merlin.pkg.tests


# the merlin package meta-data
merlin.pkg.root := packages/merlin/
merlin.pkg.stem := merlin
merlin.pkg.ext :=
merlin.pkg.drivers := merlin


# get the testsuites
include $(merlin.tests)


# end of file
