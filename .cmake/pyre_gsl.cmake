# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# build the gsl package
function(pyre_gslPackage)
  # if we have gsl
  if(${GSL_FOUND})
    # install the sources straight from the source directory
    install(
      DIRECTORY packages/gsl
      DESTINATION ${PYRE_DEST_PACKAGES}
      FILES_MATCHING PATTERN *.py
      )
  endif()
  # all done
endfunction(pyre_gslPackage)


# build the gsl module
function(pyre_gslModule)
  # if we have gsl
  if (${GSL_FOUND})
    Python_add_library(gslmodule MODULE WITH_SOABI)
    # adjust the name to match what python expects
    set_target_properties(gslmodule PROPERTIES LIBRARY_OUTPUT_NAME gsl)
    # specify the directory for the module compilation products
    pyre_library_directory(gslmodule extensions)
    # set the include directories
    target_include_directories(gslmodule PRIVATE ${GSL_INCLUDE_DIRS} ${Python_NumPy_INCLUDE_DIRS})
    # set the libraries to link against
    target_link_libraries(
      gslmodule PRIVATE
      ${GSL_LIBRARIES} pyre journal
      )
    # add the sources
    target_sources(gslmodule PRIVATE
      extensions/gsl/gsl.cc
      extensions/gsl/blas.cc
      extensions/gsl/exceptions.cc
      extensions/gsl/histogram.cc
      extensions/gsl/linalg.cc
      extensions/gsl/matrix.cc
      extensions/gsl/metadata.cc
      extensions/gsl/pdf.cc
      extensions/gsl/permutation.cc
      extensions/gsl/rng.cc
      extensions/gsl/stats.cc
      extensions/gsl/vector.cc
      )

    if (${MPI_FOUND})
      # add the MPI aware sources to the pile
      target_sources(gslmodule PRIVATE extensions/gsl/partition.cc)
      # the mpi include directories
      target_include_directories(gslmodule PRIVATE ${MPI_CXX_INCLUDE_PATH})
      # add the MPI presence indicator
      target_compile_definitions(gslmodule PRIVATE WITH_MPI)
      # and the mpi libraries
      target_link_libraries(gslmodule PRIVATE ${MPI_CXX_LIBRARIES})
    endif()

    if (${Python_NumPy_FOUND})
      # add the numpy aware sources to the pile
      target_sources(gslmodule PRIVATE extensions/gsl/numpy.cc)
      # add the MPI presence indicator
      target_compile_definitions(gslmodule PRIVATE WITH_NUMPY)
    endif()

    # copy the capsule definitions to the staging area
    configure_file(extensions/gsl/capsules.h lib/pyre/gsl COPYONLY)
    # install the extension
    install(
      TARGETS gslmodule
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/gsl
      )
    # and publish the capsules
    install(
      FILES ${CMAKE_CURRENT_SOURCE_DIR}/extensions/gsl/capsules.h
      DESTINATION ${PYRE_DEST_INCLUDE}/pyre/gsl
      )
  endif()
  # all done
endfunction(pyre_gslModule)


# end of file
