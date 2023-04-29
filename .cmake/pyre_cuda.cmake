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


# end of file
