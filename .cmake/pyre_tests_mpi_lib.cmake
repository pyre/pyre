# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the mpi tests
pyre_test_driver_mpi(tests/mpi.lib/sanity.cc 4)
pyre_test_driver_mpi(tests/mpi.lib/world.cc 4)
pyre_test_driver_mpi(tests/mpi.lib/group.cc 4)
pyre_test_driver_mpi(tests/mpi.lib/group-include.cc 7)
pyre_test_driver_mpi(tests/mpi.lib/group-exclude.cc 7)
pyre_test_driver_mpi(tests/mpi.lib/group-setops.cc 7)
pyre_test_driver_mpi(tests/mpi.lib/communicator.cc 8)
# {runtime} and {errors} say nothing about any particular rank
pyre_test_driver_mpi(tests/mpi.lib/runtime.cc 4)
pyre_test_driver_mpi(tests/mpi.lib/errors.cc 4)
# {comm-split} splits by parity, so give it an odd count to make the two halves differ in size
pyre_test_driver_mpi(tests/mpi.lib/comm-split.cc 7)
# {cartesian} lays its processes out on a two by four grid, so it needs exactly eight of them
pyre_test_driver_mpi(tests/mpi.lib/cartesian.cc 8)
# {pt2pt} puts its processes on a ring, so it needs at least two
pyre_test_driver_mpi(tests/mpi.lib/pt2pt.cc 4)
pyre_test_driver_mpi(tests/mpi.lib/collectives.cc 8)

# startup
add_test(NAME tests.mpi.lib.localhost.pre
  COMMAND ${BASH_PROGRAM} -c "cp ${PROJECT_SOURCE_DIR}/tests/mpi.lib/localhost ."
  )
# cleanup
add_test(NAME tests.mpi.lib.localhost.post
  COMMAND ${BASH_PROGRAM} -c "rm localhost"
  )

# the fixture
set_property(TEST tests.mpi.lib.localhost.pre PROPERTY
  FIXTURES_SETUP MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.localhost.post PROPERTY
  FIXTURES_CLEANUP MPI_HOSTFILE
  )

# set up the dependencies
set_property(TEST tests.mpi.lib.sanity.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.world.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.group.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.group-include.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.group-exclude.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.group-setops.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.communicator.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.runtime.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.errors.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.comm-split.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.cartesian.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.pt2pt.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST tests.mpi.lib.collectives.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )


# end of file
