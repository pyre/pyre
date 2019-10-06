# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

message("++ packages:")
message("++   source dir: ${CMAKE_CURRENT_SOURCE_DIR}")
message("++   staging dir: ${CMAKE_CURRENT_BINARY_DIR}")

# set the variables used to build the libpyre version
set(MAJOR ${REPO_MAJOR})
set(MINOR ${REPO_MINOR})
set(MICRO ${REPO_MICRO})
set(REVISION ${REPO_COMMIT})

# build the portinfo file
configure_file(
  portinfo.in portinfo
  @ONLY
  )
# buld the libpyre version file
configure_file(
  pyre/version.cc.in pyre/version.cc
  @ONLY
  )
# copy the pyre headers over to the staging area
file(
  COPY pyre
  DESTINATION ${CMAKE_CURRENT_BINARY_DIR}
  FILES_MATCHING PATTERN *.h PATTERN *.icc
  )
# copy the journal headers over to the staging area
file(
  COPY journal
  DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/pyre
  FILES_MATCHING
    PATTERN journal.h EXCLUDE
    PATTERN *.h
    PATTERN *.icc
  )
# and the journal master header with the pyre directory
file(
  COPY journal/journal.h
  DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/pyre
  )
# if we have mpi
if(MPI_FOUND)
  # copy the mpi headers
  file(
    COPY mpi
    DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/pyre
    FILES_MATCHING
      PATTERN mpi.h EXCLUDE
      PATTERN *.h
      PATTERN *.icc
    )
  # and the mpi master header with the pyre directory
  file(
    COPY mpi/mpi.h
    DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/pyre
    )
endif(MPI_FOUND)

# the libjournal target
add_library(journal SHARED)
# set the include directories
target_include_directories(
  journal PUBLIC
  ${CMAKE_CURRENT_BINARY_DIR}
  )
# add the sources
target_sources(journal
  PUBLIC
    journal/Chronicler.cc
    journal/Console.cc
    journal/Device.cc
    journal/Renderer.cc
    journal/Streaming.cc
    journal/debuginfo.cc
    journal/firewalls.cc
    journal/journal.cc
  )

# the libpyre target
add_library(pyre SHARED)
# set the include directories
target_include_directories(
  pyre PUBLIC
  ${CMAKE_CURRENT_BINARY_DIR}
  )
# add the sources
target_sources(pyre
  PUBLIC
    pyre/memory/MemoryMap.cc
    pyre/timers/Display.cc
    pyre/timers/Timer.cc
    $<BUILD_INTERFACE:pyre/version.cc>
  )
# and the link dependencies
target_link_libraries(
  pyre
  journal
  )

# install
# the portinfo file
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/portinfo
  DESTINATION ${PYRE_DEST_INCLUDE}
  )
# the libpyre and libjournal headers
install(
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pyre
  DESTINATION ${PYRE_DEST_INCLUDE}
  FILES_MATCHING PATTERN *.h PATTERN *.icc
  )
# libpyre and libjournal
install(
  TARGETS journal pyre
  LIBRARY
  )

# end of file
