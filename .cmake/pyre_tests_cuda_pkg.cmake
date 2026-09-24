# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# cuda
# sanity
pyre_test_python_testcase(tests/cuda.pkg/sanity.py)
pyre_test_python_testcase(tests/cuda.pkg/manager.py)
# the thin cublas/cusolver/curand bindings, over grids of cuda managed memory
pyre_test_python_testcase(tests/cuda.pkg/cublas.py)
pyre_test_python_testcase(tests/cuda.pkg/grid_interface.py)
pyre_test_python_testcase(tests/cuda.pkg/grid_inplace.py)


# end of file
