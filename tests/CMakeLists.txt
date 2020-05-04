# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


# the pure python tests
include(pyre_tests_python)
# the pyre tests
include(pyre_tests_pyre)
include(pyre_tests_journal)

# sqlite
include(pyre_tests_sqlite)

# if we have MPI support
if(MPI_FOUND)
  include(pyre_tests_mpi)
endif()

# if we have GSL support
if(GSL_FOUND)
  include(pyre_tests_gsl)
endif()


# end of file
