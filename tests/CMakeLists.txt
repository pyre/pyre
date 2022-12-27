# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved
#


# pure python
include(pyre_tests_python)

# pyre
include(pyre_tests_pyre_lib)
include(pyre_tests_pyre_pkg)

# journal
include(pyre_tests_journal_lib)
include(pyre_tests_journal_pkg)
include(pyre_tests_journal_ext)
include(pyre_tests_journal_api)

# merlin; disable for now so CI doesn't fail while restructuring the package
# include(pyre_tests_merlin_pkg)

# sqlite
include(pyre_tests_sqlite_pkg)

# if we have CUDA and the user cares
if(WITH_CUDA)
  include(pyre_tests_cuda_pkg)
endif()

# if we have MPI support
if(MPI_FOUND)
  include(pyre_tests_mpi_pkg)
  include(pyre_tests_mpi_lib)
endif()

# if we have GSL support
if(GSL_FOUND)
  include(pyre_tests_gsl_pkg)
endif()

# if we have postgres support
if(PostgreSQL_FOUND)
  include(pyre_tests_postgres_ext)
endif()


# end of file
