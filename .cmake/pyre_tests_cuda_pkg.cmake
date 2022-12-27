# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# cuda
# sanity
pyre_test_python_testcase(cuda.pkg/sanity.py)
pyre_test_python_testcase(cuda.pkg/extension.py)
pyre_test_python_testcase(cuda.pkg/manager.py)


# end of file
