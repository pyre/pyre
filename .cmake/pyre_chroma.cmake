# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# stage and install the header-only chroma library
function(pyre_chromaLib)
  # copy the chroma headers into the staging area, under the pyre namespace
  file(GLOB_RECURSE files
       RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/lib/chroma
       CONFIGURE_DEPENDS
       lib/chroma/*.h lib/chroma/*.icc
       )
  foreach(file ${files})
    # the gateway header sits at pyre/chroma.h, not under pyre/chroma/
    if("${file}" STREQUAL "chroma.h")
      continue()
    endif()
    configure_file(lib/chroma/${file} lib/pyre/chroma/${file} COPYONLY)
  endforeach()

  # and the chroma master header within the pyre directory
  configure_file(lib/chroma/chroma.h lib/pyre/chroma.h COPYONLY)

  # the staged headers ship with the rest of {lib/pyre} via {pyre_pyreLib}
  # all done
endfunction(pyre_chromaLib)


# end of file
