# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the mpi tests
pyre_test_driver_mpi(mpi.lib/sanity.cc 4)
pyre_test_driver_mpi(mpi.lib/world.cc 4)
pyre_test_driver_mpi(mpi.lib/group.cc 4)
pyre_test_driver_mpi(mpi.lib/group-include.cc 7)
pyre_test_driver_mpi(mpi.lib/group-exclude.cc 7)
pyre_test_driver_mpi(mpi.lib/group-setops.cc 7)
pyre_test_driver_mpi(mpi.lib/communicator.cc 8)

# startup
add_test(NAME mpi.lib.localhost.pre
  COMMAND ${BASH_PROGRAM} -c "cp ${PYRE_TESTSUITE_DIR}/mpi.lib/localhost ."
  )
# cleanup
add_test(NAME mpi.lib.localhost.post
  COMMAND ${BASH_PROGRAM} -c "rm localhost"
  )

# the fixture
set_property(TEST mpi.lib.localhost.pre PROPERTY
  FIXTURES_SETUP MPI_HOSTFILE
  )
set_property(TEST mpi.lib.localhost.post PROPERTY
  FIXTURES_CLEANUP MPI_HOSTFILE
  )

# set up the dependencies
set_property(TEST mpi.lib.sanity.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST mpi.lib.world.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST mpi.lib.group.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST mpi.lib.group-include.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST mpi.lib.group-exclude.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST mpi.lib.group-setops.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )
set_property(TEST mpi.lib.communicator.cc PROPERTY
  FIXTURES_REQUIRED MPI_HOSTFILE
  )


# end of file
