# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# set the variables used in the package meta-data files
set(MAJOR ${REPO_MAJOR})
set(MINOR ${REPO_MINOR})
set(MICRO ${REPO_MICRO})
set(REVISION ${REPO_COMMIT})
string(TIMESTAMP TODAY)

# pyre
# install the sources straight from the source directory
install(
  DIRECTORY pyre
  DESTINATION ${PYRE_DEST_PACKAGES}
  FILES_MATCHING PATTERN *.py
  )
# build the package meta-data
configure_file(
  pyre/meta.py.in pyre/meta.py
  @ONLY
  )
# install the generated package meta-data file
install(
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pyre
  DESTINATION ${PYRE_DEST_PACKAGES}
  FILES_MATCHING PATTERN *.py
  )

# journal
# install the sources straight from the source directory
install(
  DIRECTORY journal
  DESTINATION ${PYRE_DEST_PACKAGES}
  FILES_MATCHING PATTERN *.py
  )

# merlin
# install the sources straight from the source directory
install(
  DIRECTORY merlin
  DESTINATION ${PYRE_DEST_PACKAGES}
  FILES_MATCHING PATTERN *.py
  )
# build the package meta-data
configure_file(
  merlin/meta.py.in merlin/meta.py
  @ONLY
  )
# install the generated package meta-data file
install(
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/merlin
  DESTINATION ${PYRE_DEST_PACKAGES}
  FILES_MATCHING PATTERN *.py
  )

# if the user requested CUDA support
if(WITH_CUDA)
  # install the sources straight from the source directory
  install(
    DIRECTORY cuda
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
endif()

# if we have gsl
if(${GSL_FOUND})
  # install the sources straight from the source directory
  install(
    DIRECTORY gsl
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
endif()

# if we have mpi
if(${MPI_FOUND})
  # install the sources straight from the source directory
  install(
    DIRECTORY mpi
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    mpi/meta.py.in mpi/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/mpi
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
endif()

# end of file
