# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the survey package test suite
pyre_test_python_testcase(tests/survey.pkg/sanity.py)
pyre_test_python_testcase(tests/survey.pkg/input.py)
pyre_test_python_testcase(tests/survey.pkg/confirm.py)
pyre_test_python_testcase(tests/survey.pkg/selection.py)
pyre_test_python_testcase(tests/survey.pkg/configure.py)
pyre_test_python_testcase(tests/survey.pkg/configure_facility.py)


# end of file
