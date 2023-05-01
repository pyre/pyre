# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


function(pyre_mpiPackage)
  # if we have mpi
  if(${MPI_FOUND})
    # install the sources straight from the source directory
    install(
      DIRECTORY packages/mpi
      DESTINATION ${PYRE_DEST_PACKAGES}
      FILES_MATCHING PATTERN *.py
      )
    # build the package meta-data
    configure_file(
      packages/mpi/meta.py.in packages/mpi/meta.py
      @ONLY
      )
    # install the generated package meta-data file
    install(
      DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/packages/mpi
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
    file(GLOB_RECURSE files
         RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/lib/mpi
         CONFIGURE_DEPENDS
         lib/mpi/*.h lib/mpi/*.icc
         )
    foreach(file ${files})
      # skip the special header
      if("${file}" STREQUAL "mpi.h")
        continue()
      endif()
      configure_file(lib/mpi/${file} lib/pyre/mpi/${file} COPYONLY)
    endforeach()

    # and the mpi master header with the pyre directory
    configure_file(lib/mpi/mpi.h lib/pyre/mpi.h COPYONLY)

    # the mpi target (INTERFACE since it is header-only)
    add_library(mpi INTERFACE)
    # specify the directory for the library compilation products
    pyre_library_directory(mpi lib)
    target_link_libraries(mpi INTERFACE pyre MPI::MPI_CXX)
    target_include_directories(mpi INTERFACE
      $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/lib>
      $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
      )
    add_library(pyre::mpi ALIAS mpi)

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
    # specify the directory for the module compilation products
    pyre_library_directory(mpimodule extensions)
    # set the libraries to link against
    target_link_libraries(
      mpimodule PRIVATE pyre::mpi journal
      )
    # add the sources
    target_sources(mpimodule PRIVATE
      extensions/mpi/mpi.cc
      extensions/mpi/communicators.cc
      extensions/mpi/exceptions.cc
      extensions/mpi/groups.cc
      extensions/mpi/metadata.cc
      extensions/mpi/ports.cc
      extensions/mpi/startup.cc
      )
    # copy the capsule definitions to the staging area
    configure_file(extensions/mpi/capsules.h lib/pyre/mpi COPYONLY)
    # install the extension
    install(
      TARGETS mpimodule
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/mpi
      )
    # and publish the capsules
    install(
      FILES ${CMAKE_CURRENT_SOURCE_DIR}/extensions/mpi/capsules.h
      DESTINATION ${PYRE_DEST_INCLUDE}/pyre/mpi
      )
  endif()
  # all done
endfunction(pyre_mpiModule)


# end of file
