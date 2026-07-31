# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


function(pyre_cudaPackage)
  # if the user requested CUDA support
  if(WITH_CUDA)
    # install the sources straight from the source directory
    install(
      DIRECTORY packages/cuda
      DESTINATION ${PYRE_DEST_PACKAGES}
      FILES_MATCHING PATTERN *.py
      )
  endif()
  # all done
endfunction(pyre_cudaPackage)


# the pyre cuda headers
function(pyre_cudaLib)
  # if the user requested CUDA support
  if(WITH_CUDA)
    # copy the cuda headers
    file(GLOB_RECURSE files
         RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/lib/cuda
         CONFIGURE_DEPENDS
         lib/cuda/*.h lib/cuda/*.icc
         )
    foreach(file ${files})
      # skip the special header
      if("${file}" STREQUAL "cuda.h")
        continue()
      endif()
      configure_file(lib/cuda/${file} lib/pyre/cuda/${file} COPYONLY)
    endforeach()

    # and the cuda master header within the pyre directory
    configure_file(lib/cuda/cuda.h lib/pyre/cuda.h COPYONLY)

    # the {cuda} target (INTERFACE since it is header-only)
    add_library(cuda INTERFACE)
    # specify the directory for the library compilation products
    pyre_library_directory(cuda lib)
    # its headers reach {pyre/memory.h} and {pyre/journal.h}, so it stands on {pyre}, which is
    # also what puts our own headers on the consumer's include path; the cuda runtime arrives
    # as an imported target, which carries its own include path along with the library
    target_link_libraries(cuda INTERFACE pyre CUDA::cudart)
    # set the include directories; the toolkit headers ride in on {CUDA::cudart}, so all that
    # is left is finding our own, in the build tree and in the prefix
    target_include_directories(cuda INTERFACE
      $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/lib>
      $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
      )
    add_library(pyre::cuda ALIAS cuda)

    # hand it downstream; the headers ship either way, so without this a consumer finds
    # {pyre/cuda.h} in the prefix and has nothing to link it against
    install(
      TARGETS cuda
      EXPORT pyre-targets
      )
    pyre_exportTarget(cuda cuda)
    # this target names {CUDA::cudart}, so a consumer that asks for the add-on has to be able
    # to resolve it; teach the generated configuration where it comes from
    pyre_exportOptionalRequirement(cuda CUDAToolkit CUDA::cudart)
  endif()
  # all done
endfunction(pyre_cudaLib)


# build the cuda extension module
function(pyre_cudaModule)
  # if the user requested CUDA support
  if(WITH_CUDA)
    # the cuda bindings
    Python_add_library(cudamodule MODULE WITH_SOABI)
    # adjust the name to match what python expects
    set_target_properties(cudamodule PROPERTIES LIBRARY_OUTPUT_NAME cuda)
    # specify the directory for the module compilation products
    pyre_library_directory(cudamodule extensions)
    # set the libraries to link against; {CUDA::cudart} brings the toolkit headers with it,
    # so the module needs no include directories of its own
    target_link_libraries(cudamodule PRIVATE pyre journal pybind11::module CUDA::cudart)
    # add the sources
    target_sources(cudamodule PRIVATE
      extensions/cuda/cuda.cc
      extensions/cuda/device.cc
      extensions/cuda/discover.cc
      extensions/cuda/exceptions.cc
      extensions/cuda/metadata.cc
    )

    # install the cuda extensions
    install(
      TARGETS cudamodule
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/cuda
      )
  endif()
endfunction(pyre_cudaModule)


# build the cuda kernel associated with this {driverfile}
function(pyre_kernel_target kernelobject driverfile)
    # extract the driver directory
    get_filename_component(driver_directory ${driverfile} DIRECTORY)
    # extract the driver basename
    get_filename_component(driver_basename ${driverfile} NAME_WE)
    # assemble the cu filename associated with this {driverfile}
    set(cudafile "${driver_directory}/${driver_basename}.cu")
    # generate the name of the target with the cuda kernel
    pyre_target(kernelobject ${cudafile})
    # rename the kernel target to distinguish it from the driver target
    set(kernelobject "${kernelobject}_kernel")
    # propagate definition of variable to parent scope
    set(kernelobject "${kernelobject}" PARENT_SCOPE)
    # sign up the kernel target for build based on the cuda source file
    add_library("${kernelobject}" STATIC ${cudafile})
  # all done
endfunction()

# end of file
