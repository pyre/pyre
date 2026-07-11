# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

#
# gsl extension: these drivers import the {libgsl} bindings directly, bypassing the {gsl}
# package shim, so a failure isolates the c++ layer
#
# sanity
pyre_test_python_testcase(tests/gsl.ext/sanity.py)
# the bound data types
pyre_test_python_testcase(tests/gsl.ext/vector.py)
pyre_test_python_testcase(tests/gsl.ext/matrix.py)
pyre_test_python_testcase(tests/gsl.ext/permutation.py)
pyre_test_python_testcase(tests/gsl.ext/histogram.py)
pyre_test_python_testcase(tests/gsl.ext/rng.py)
# the flag enumerations
pyre_test_python_testcase(tests/gsl.ext/enums.py)


# end of file
