# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


function(pyre_mpiPackage)
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
  # all done
endfunction(pyre_mpiPackage)


# the pyre mpi headers
function(pyre_mpiLib)
  # if we have mpi
  if(MPI_FOUND)
    # copy the mpi headers

    # the mpi target (INTERFACE since it is header-only)
    add_library(mpi INTERFACE)
    target_link_libraries(mpi INTERFACE pyre MPI::MPI_CXX)
    target_include_directories(mpi INTERFACE
      $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
      $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
      )
    add_library(pyre::mpi ALIAS mpi)

    file(GLOB_RECURSE
         RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/mpi
         CONFIGURE_DEPENDS
         *.h *.icc
         )
    foreach(file ${files})
      # skip the special header
      if("${file}" STREQUAL "mpi.h")
        continue()
      endif()
      configure_file(mpi/${file} pyre/mpi/${file} COPYONLY)
    endforeach()
    # and the mpi master header with the pyre directory
    configure_file(mpi/mpi.h pyre/mpi.h COPYONLY)
  endif(MPI_FOUND)
  # all done
endfunction(pyre_mpiLib)


# build the mpi module
function(pyre_mpiModule)
  # if we have mpi
  if (${MPI_FOUND})
    Python_add_library(mpimodule MODULE)
    # adjust the name to match what python expects
    set_target_properties(mpimodule PROPERTIES LIBRARY_OUTPUT_NAME mpi)
    set_target_properties(mpimodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
    # set the libraries to link against
    target_link_libraries(
      mpimodule PRIVATE pyre::mpi journal
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
    # copy the capsule definitions to the staging area
    configure_file(mpi/capsules.h ../lib/pyre/mpi/ COPYONLY)
    # install the extension
    install(
      TARGETS mpimodule
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/mpi
      )
    # and publish the capsules
    install(
      FILES ${CMAKE_CURRENT_SOURCE_DIR}/mpi/capsules.h
      DESTINATION ${PYRE_DEST_INCLUDE}/pyre/mpi
      )
  endif()
  # all done
endfunction(pyre_mpiModule)


# end of file
