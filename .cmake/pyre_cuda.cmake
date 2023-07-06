# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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
      configure_file(lib/cuda/${file} lib/pyre/cuda/${file} COPYONLY)
    endforeach()
  endif()
  # all done
endfunction(pyre_cudaLib)


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
