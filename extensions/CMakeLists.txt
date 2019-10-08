# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# set the variables used to build the libpyre version
set(MAJOR ${REPO_MAJOR})
set(MINOR ${REPO_MINOR})
set(MICRO ${REPO_MICRO})
set(REVISION ${REPO_COMMIT})

# journal
Python3_add_library(journalmodule MODULE)
# turn on the core macro
set_target_properties(journalmodule PROPERTIES COMPILE_DEFINITIONS PYRE_CORE)
# adjust the name to match what python expects
set_target_properties(journalmodule PROPERTIES LIBRARY_OUTPUT_NAME journal)
set_target_properties(journalmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
# set the include directories
target_include_directories(journalmodule PRIVATE ${CMAKE_BINARY_DIR}/lib)
# set the libraries to link against
target_link_libraries(journalmodule PRIVATE journal)
# add the sources
target_sources(journalmodule PRIVATE
  journal/journal.cc
  journal/DeviceProxy.cc
  journal/channels.cc
  journal/exceptions.cc
  journal/init.cc
  journal/metadata.cc
  journal/tests.cc
  )
# install
install(
  TARGETS journalmodule
  LIBRARY
  DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/journal
  )

# host
Python3_add_library(hostmodule MODULE)
# adjust the name to match what python expects
set_target_properties(hostmodule PROPERTIES LIBRARY_OUTPUT_NAME host)
set_target_properties(hostmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
# set the include directories
target_include_directories(hostmodule PRIVATE ${CMAKE_BINARY_DIR}/lib)
# set the libraries to link against
target_link_libraries(hostmodule PRIVATE pyre journal)
# add the sources
target_sources(hostmodule PRIVATE
  host/host.cc
  host/cpu.cc
  host/metadata.cc
  )

# timers
Python3_add_library(timersmodule MODULE)
# adjust the name to match what python expects
set_target_properties(timersmodule PROPERTIES LIBRARY_OUTPUT_NAME timers)
set_target_properties(timersmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
# set the include directories
target_include_directories(timersmodule PRIVATE ${CMAKE_BINARY_DIR}/lib)
# set the libraries to link against
target_link_libraries(timersmodule PRIVATE pyre journal)
# add the sources
target_sources(timersmodule PRIVATE
  timers/timers.cc
  timers/display.cc
  timers/metadata.cc
  )

# install the pyre extensions
install(
  TARGETS hostmodule timersmodule
  LIBRARY
  DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/pyre/extensions
  )

# if we have mpi
if (${MPI_FOUND})
  Python3_add_library(mpimodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(mpimodule PROPERTIES LIBRARY_OUTPUT_NAME mpi)
  set_target_properties(mpimodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
  # set the include directories
  target_include_directories(
    mpimodule PRIVATE
    ${MPI_CXX_INCLUDE_PATH} ${CMAKE_BINARY_DIR}/lib)
  # set the libraries to link against
  target_link_libraries(
    mpimodule PRIVATE
    ${MPI_CXX_LIBRARIES} pyre journal
    )
  # add the sources
  target_sources(mpimodule PRIVATE
    mpi/mpi.cc
    mpi/communicators.cc
    mpi/exceptions.cc
    mpi/groups.cc
    mpi/metadata.cc
    mpi/ports.cc
    mpi/startup.cc
    )
  # copy the capsule definitions to staging area
  file(
    COPY mpi/capsules.h
    DESTINATION ${CMAKE_BINARY_DIR}/lib/pyre/mpi
    )

  # install the extension
  install(
    TARGETS mpimodule
    LIBRARY
    DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/mpi
    )
  # and publish the capsules
  install(
    FILES ${CMAKE_CURRENT_SOURCE_DIR}/mpi/capsules.h
    DESTINATION ${CMAKE_INSTALL_PREFIX}/include/pyre/mpi
    )
endif()

# if we have gsl
if (${GSL_FOUND})
  Python3_add_library(gslmodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(gslmodule PROPERTIES LIBRARY_OUTPUT_NAME gsl)
  set_target_properties(gslmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
  # set the include directories
  target_include_directories(
    gslmodule PRIVATE
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS} ${CMAKE_BINARY_DIR}/lib
    )
  # set the libraries to link against
  target_link_libraries(
    gslmodule PRIVATE
    ${GSL_LIBRARIES} pyre journal
    )
  # add the sources
  target_sources(gslmodule PRIVATE
    gsl/gsl.cc
    gsl/blas.cc
    gsl/exceptions.cc
    gsl/histogram.cc
    gsl/linalg.cc
    gsl/matrix.cc
    gsl/metadata.cc
    gsl/numpy.cc
    gsl/pdf.cc
    gsl/permutation.cc
    gsl/rng.cc
    gsl/stats.cc
    gsl/vector.cc
    )

  if (${MPI_FOUND})
    # add the MPI aware sources to the pile
    target_sources(gslmodule PRIVATE gsl/partition.cc)
    # the mpi include directories
    target_include_directories(gslmodule PRIVATE ${MPI_CXX_INCLUDE_PATH})
    # and the mpi libraries
    target_link_libraries(gslmodule PRIVATE ${MPI_CXX_LIBRARIES})
  endif()

  # install the extension
  install(
    TARGETS gslmodule
    LIBRARY
    DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/gsl
    )
endif()

# end of file
