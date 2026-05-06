# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# initialize BLAS: select the vendor and discover the library
function(pyre_blasInit)
  # let the user pick the BLAS vendor; empty string triggers auto-detection
  set(BLA_VENDOR "" CACHE STRING
    "BLAS vendor (e.g. OpenBLAS, ATLAS, Apple, MKL, FlexiBLAS, Generic); empty for auto-detect"
    )
  # valid choices for cmake-gui drop-down
  set_property(CACHE BLA_VENDOR PROPERTY STRINGS
    "" OpenBLAS ATLAS Apple MKL FlexiBLAS FLAME Goto IBMESSL NAS Generic
    )
  # discover the library
  find_package(BLAS)
  # pick the link target: prefer an external BLAS, fall back to the one bundled with GSL
  if(${BLAS_FOUND})
    set(BLAS_LIB_IMPORT BLAS::BLAS PARENT_SCOPE)
    message(STATUS "Found BLAS: ${BLAS_LIBRARIES} (vendor: '${BLA_VENDOR}')")
  else()
    set(BLAS_LIB_IMPORT GSL::gslcblas PARENT_SCOPE)
    message(STATUS "BLAS not found; will use GSL::gslcblas (vendor: '${BLA_VENDOR}')")
  endif()
  # all done
endfunction(pyre_blasInit)


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
  # resolve the BLAS link target
  pyre_blasInit()
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
      GSL::gsl ${BLAS_LIB_IMPORT} pyre journal pybind11::module
      )
    # add the sources
    target_sources(gslmodule PRIVATE
      extensions/gsl/__init__.cc
      extensions/gsl/blas.cc
      extensions/gsl/histogram.cc
      extensions/gsl/linalg.cc
      extensions/gsl/matrix.cc
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

    # install the extension
    install(
      TARGETS gslmodule
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/gsl
      )
  endif()
  # all done
endfunction(pyre_gslModule)


# end of file
