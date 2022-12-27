# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# generate the portinfo file
function(pyre_portinfo)
  # inject the platform information and move it to the staging area
  # this is the C++ version
  configure_file(
    portinfo.in portinfo
    @ONLY
    )
  # install the portinfo file
  install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/portinfo
    DESTINATION ${PYRE_DEST_INCLUDE}
    )

  # repeat with the C version
  configure_file(
    portinfo.in portinfo.h
    @ONLY
    )
  # install the portinfo file
  install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/portinfo.h
    DESTINATION ${PYRE_DEST_INCLUDE}
    )

  # all done
endfunction(pyre_portinfo)


# build the pyre package
function(pyre_pyrePackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY pyre
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    pyre/meta.py.in pyre/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pyre
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(pyre_pyrePackage)


# build the pyre libraries
function(pyre_pyreLib)
  # build the libpyre version file
  configure_file(
    pyre/version.h.in pyre/version.h
    @ONLY
    )
  configure_file(
    pyre/version.cc.in pyre/version.cc
    @ONLY
    )
  # copy the pyre headers over to the staging area
  file(GLOB_RECURSE files
       RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/pyre
       CONFIGURE_DEPENDS
       *.h *.icc
       )
  foreach(file ${files})
    configure_file(pyre/${file} pyre/${file} COPYONLY)
  endforeach()

  # the libpyre target
  add_library(pyre SHARED)
  # set the include directories
  target_include_directories(
    pyre PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
    )
  # add the sources
  target_sources(pyre
    PRIVATE
    pyre/memory/FileMap.cc
    ${CMAKE_CURRENT_BINARY_DIR}/pyre/version.cc
    )
  # and the link dependencies
  target_link_libraries(
    pyre
    journal
    )

  # install all the pyre headers
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pyre
    DESTINATION ${PYRE_DEST_INCLUDE}
    FILES_MATCHING PATTERN *.h PATTERN *.icc
    )

  # libpyre and libjournal
  install(
    TARGETS pyre
    EXPORT pyre-targets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )

  # all done
endfunction(pyre_pyreLib)


# build the pyre extension modules
function(pyre_pyreModule)
  # the pyre bindings
  Python_add_library(pyremodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(pyremodule PROPERTIES LIBRARY_OUTPUT_NAME pyre)
  set_target_properties(pyremodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
  # set the libraries to link against
  target_link_libraries(pyremodule PRIVATE pyre journal pybind11::module)
  # add the sources
  target_sources(pyremodule PRIVATE
    pyre/pyre.cc
    pyre/api.cc
    pyre/grid/grid.cc
    pyre/grid/indices.cc
    pyre/grid/grids.cc
    pyre/grid/orders.cc
    pyre/grid/packings.cc
    pyre/grid/shapes.cc
    pyre/memory/memory.cc
    pyre/memory/maps.cc
    pyre/timers/timers.cc
    pyre/timers/process_timers.cc
    pyre/timers/wall_timers.cc
    pyre/viz/viz.cc
    pyre/viz/bmp.cc
)

  # host
  Python_add_library(hostmodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(hostmodule PROPERTIES LIBRARY_OUTPUT_NAME host)
  set_target_properties(hostmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
  # set the libraries to link against
  target_link_libraries(hostmodule PRIVATE pyre journal)
  # add the sources
  target_sources(hostmodule PRIVATE
    host/host.cc
    host/cpu.cc
    host/metadata.cc
    )

  # install the pyre extensions
  install(
    TARGETS hostmodule pyremodule
    LIBRARY
    DESTINATION ${PYRE_DEST_PACKAGES}/pyre/extensions
    )
endfunction(pyre_pyreModule)


# the scripts
function(pyre_pyreBin)
  # the pyre enhanced interpreter
  add_executable(python.pyre)
  # its sources
  target_sources(python.pyre PRIVATE
    python.cc
    )
  # and libraries
  target_link_libraries(python.pyre Python::Python)

  # install the custom python
  install(
    TARGETS python.pyre
    RUNTIME
    DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
  # install the scripts
  install(
    PROGRAMS pyre pyre-config merlin smith.pyre
    DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
  # all done
endfunction(pyre_pyreBin)


# the configuration files
function(pyre_pyreDefaults)
  # install the configuration files
  install(
    DIRECTORY pyre merlin
    DESTINATION share
  )
  # all done
endfunction(pyre_pyreDefaults)


# end of file
