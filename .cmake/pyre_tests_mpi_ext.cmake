# -*- cmake -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


#
# the mpi bindings
#
pyre_test_python_testcase(tests/mpi.ext/sanity.py)
pyre_test_python_testcase(tests/mpi.ext/libmpi_sanity.py)
pyre_test_python_testcase(tests/mpi.ext/libmpi_enums.py)
pyre_test_python_testcase(tests/mpi.ext/libmpi_exceptions.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_exceptions.py 8)
pyre_test_python_testcase(tests/mpi.ext/libmpi_runtime.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_runtime.py 8)
pyre_test_python_testcase(tests/mpi.ext/libmpi_communicator.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_communicator.py 8)
pyre_test_python_testcase(tests/mpi.ext/libmpi_group.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_group.py 7)
pyre_test_python_testcase(tests/mpi.ext/libmpi_reductions.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_reductions.py 8)
pyre_test_python_testcase(tests/mpi.ext/libmpi_collectives.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_collectives.py 8)
pyre_test_python_testcase(tests/mpi.ext/libmpi_port.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_port.py 4)
pyre_test_python_testcase(tests/mpi.ext/libmpi_nonblocking.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_nonblocking.py 4)
pyre_test_python_testcase(tests/mpi.ext/libmpi_cartesian.py)
pyre_test_python_testcase_mpi(tests/mpi.ext/libmpi_cartesian.py 8)


# end of file
