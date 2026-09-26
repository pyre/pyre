# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# cuda
# sanity
pyre_test_python_testcase(tests/cuda.pkg/sanity.py)
pyre_test_python_testcase(tests/cuda.pkg/extension.py)
pyre_test_python_testcase(tests/cuda.pkg/manager.py)
pyre_test_python_testcase(tests/cuda.pkg/exceptions.py)
pyre_test_python_testcase(tests/cuda.pkg/grid_managed.py)
pyre_test_python_testcase(tests/cuda.pkg/grid_interface.py)
pyre_test_python_testcase(tests/cuda.pkg/grid_inplace.py)
pyre_test_python_testcase(tests/cuda.pkg/grid_sync.py)
pyre_test_python_testcase(tests/cuda.pkg/grid_mixed.py)
pyre_test_python_testcase(tests/cuda.pkg/cublas.py)
pyre_test_python_testcase(tests/cuda.pkg/cusolver.py)
pyre_test_python_testcase(tests/cuda.pkg/curand.py)
pyre_test_python_testcase(tests/cuda.pkg/handles.py)


# end of file
