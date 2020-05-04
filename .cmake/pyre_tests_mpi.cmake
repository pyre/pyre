# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# mpi
#
pyre_test_python_testcase(mpi/sanity.py)
pyre_test_python_testcase(mpi/extension.py)
pyre_test_python_testcase_mpi(mpi/extension.py 8)
pyre_test_python_testcase(mpi/world.py)
pyre_test_python_testcase_mpi(mpi/world.py 8)
pyre_test_python_testcase_mpi(mpi/group.py 7)
pyre_test_python_testcase_mpi(mpi/group_include.py 7)
pyre_test_python_testcase_mpi(mpi/group_exclude.py 7)
pyre_test_python_testcase_mpi(mpi/group_setops.py 7)
pyre_test_python_testcase_mpi(mpi/restrict.py 7)
pyre_test_python_testcase_mpi(mpi/bcast.py 8)
pyre_test_python_testcase_mpi(mpi/sum.py 8)
pyre_test_python_testcase_mpi(mpi/product.py 8)
pyre_test_python_testcase_mpi(mpi/max.py 8)
pyre_test_python_testcase_mpi(mpi/min.py 8)
pyre_test_python_testcase_mpi(mpi/port.py 7)
pyre_test_python_testcase(mpi/mpirun.py)
pyre_test_python_testcase(mpi/slurm.py)



# end of file
