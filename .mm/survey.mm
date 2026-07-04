# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# survey builds a pure-python package
survey.packages := survey.pkg
# with no libraries or extensions
survey.libraries :=
survey.extensions :=
# and a test suite
survey.tests := survey.pkg.tests

# the survey package meta-data
survey.pkg.root := packages/survey/
survey.pkg.stem := survey
survey.pkg.ext :=


# get the test suites
include $(survey.tests)


# end of file
