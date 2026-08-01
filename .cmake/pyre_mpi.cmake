# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


function(pyre_mpiPackage)
  # the pure-python {mpi} package ships unconditionally: it degrades to a trivial single-process
  # communicator when the {libmpi} bindings are absent, so code written against it runs anywhere
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

    # hand it downstream; the headers ship either way, so without this a consumer finds
    # {pyre/mpi.h} in the prefix and has nothing to link it against
    install(
      TARGETS mpi
      EXPORT pyre-targets
      )
    pyre_exportTarget(mpi mpi)
    # its link interface names the mpi imported target, so a consumer that asks for this
    # component has to be able to resolve it
    pyre_exportOptionalRequirement(mpi MPI MPI::MPI_CXX "COMPONENTS CXX")

  endif(MPI_FOUND)
  # all done
endfunction(pyre_mpiLib)


# build the mpi module
function(pyre_mpiModule)
  # if we have mpi
  if (MPI_FOUND)
    Python_add_library(mpimodule MODULE WITH_SOABI)
    # adjust the name to match what python expects
    set_target_properties(mpimodule PROPERTIES LIBRARY_OUTPUT_NAME libmpi)
    # specify the directory for the module compilation products
    pyre_library_directory(mpimodule extensions)
    # set the libraries to link against
    target_link_libraries(
      mpimodule PRIVATE pyre::mpi journal pybind11::module
      )
    # add the sources
    target_sources(mpimodule PRIVATE
      extensions/mpi/__init__.cc
      extensions/mpi/api.cc
      extensions/mpi/Cartesian.cc
      extensions/mpi/Communicator.cc
      extensions/mpi/enums.cc
      extensions/mpi/exceptions.cc
      extensions/mpi/Group.cc
      extensions/mpi/Port.cc
      extensions/mpi/Request.cc
      extensions/mpi/Status.cc
      extensions/mpi/utilities.cc
      )
    # install the extension
    install(
      TARGETS mpimodule
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/mpi
      )
  endif()
  # all done
endfunction(pyre_mpiModule)


# end of file
