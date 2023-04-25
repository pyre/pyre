# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# mpi
#
pyre_test_python_testcase(tests/mpi.pkg/sanity.py)
pyre_test_python_testcase(tests/mpi.pkg/extension.py)
pyre_test_python_testcase_mpi(tests/mpi.pkg/extension.py 8)
pyre_test_python_testcase(tests/mpi.pkg/world.py)
pyre_test_python_testcase_mpi(tests/mpi.pkg/world.py 8)
pyre_test_python_testcase_mpi(tests/mpi.pkg/group.py 7)
pyre_test_python_testcase_mpi(tests/mpi.pkg/group_include.py 7)
pyre_test_python_testcase_mpi(tests/mpi.pkg/group_exclude.py 7)
pyre_test_python_testcase_mpi(tests/mpi.pkg/group_setops.py 7)
pyre_test_python_testcase_mpi(tests/mpi.pkg/restrict.py 7)
pyre_test_python_testcase_mpi(tests/mpi.pkg/bcast.py 8)
pyre_test_python_testcase_mpi(tests/mpi.pkg/sum.py 8)
pyre_test_python_testcase_mpi(tests/mpi.pkg/product.py 8)
pyre_test_python_testcase_mpi(tests/mpi.pkg/max.py 8)
pyre_test_python_testcase_mpi(tests/mpi.pkg/min.py 8)
pyre_test_python_testcase_mpi(tests/mpi.pkg/port.py 7)
pyre_test_python_testcase(tests/mpi.pkg/mpirun.py)
pyre_test_python_testcase(tests/mpi.pkg/slurm.py)


# end of file
