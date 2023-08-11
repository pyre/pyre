# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# generate the portinfo file
function(pyre_portinfo)
  # inject the platform information and move it to the staging area
  # this is the C++ version
  configure_file(
    lib/portinfo.in lib/portinfo
    @ONLY
    )
  # install the portinfo file
  install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/lib/portinfo
    DESTINATION ${PYRE_DEST_INCLUDE}
    )

  # repeat with the C version
  configure_file(
    lib/portinfo.in lib/portinfo.h
    @ONLY
    )
  # install the portinfo file
  install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/lib/portinfo.h
    DESTINATION ${PYRE_DEST_INCLUDE}
    )

  # all done
endfunction(pyre_portinfo)


# build the pyre package
function(pyre_pyrePackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY packages/pyre
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    packages/pyre/meta.py.in packages/pyre/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/packages/pyre
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(pyre_pyrePackage)


# build the pyre libraries
function(pyre_pyreLib)
  # build the libpyre version file
  configure_file(
    lib/pyre/version.h.in lib/pyre/version.h
    @ONLY
    )
  configure_file(
    lib/pyre/version.cc.in lib/pyre/version.cc
    @ONLY
    )
  # copy the pyre headers over to the staging area
  file(GLOB_RECURSE files
       RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/lib/pyre
       CONFIGURE_DEPENDS
       lib/pyre/*.h lib/pyre/*.icc
       )
  foreach(file ${files})
    configure_file(lib/pyre/${file} lib/pyre/${file} COPYONLY)
  endforeach()

  # the libpyre target
  add_library(pyre SHARED)
  # specify the directory for the library compilation products
  pyre_library_directory(pyre lib)
  # set the include directories
  target_include_directories(
    pyre PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/lib>
    $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
    )
  # add the sources
  target_sources(pyre
    PRIVATE
    lib/pyre/memory/FileMap.cc
    ${CMAKE_CURRENT_BINARY_DIR}/lib/pyre/version.cc
    )
  # and the link dependencies
  target_link_libraries(
    pyre
    journal
    )

  # install all the pyre headers
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib/pyre
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
  # specify the directory for the module compilation products
  pyre_library_directory(pyremodule extensions)
  # set the libraries to link against
  target_link_libraries(pyremodule PRIVATE pyre journal pybind11::module)
  # add the sources
  target_sources(pyremodule PRIVATE
    extensions/pyre/__init__.cc
    extensions/pyre/api.cc
    extensions/pyre/grid/__init__.cc
    extensions/pyre/grid/indices.cc
    extensions/pyre/grid/grids.cc
    extensions/pyre/grid/orders.cc
    extensions/pyre/grid/packings.cc
    extensions/pyre/grid/shapes.cc
    extensions/pyre/memory/__init__.cc
    extensions/pyre/memory/heaps.cc
    extensions/pyre/memory/maps.cc
    extensions/pyre/timers/__init__.cc
    extensions/pyre/timers/process_timers.cc
    extensions/pyre/timers/wall_timers.cc
    extensions/pyre/viz/__init__.cc
    extensions/pyre/viz/bmp.cc
  )

  # host
  Python_add_library(hostmodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(hostmodule PROPERTIES LIBRARY_OUTPUT_NAME host)
  set_target_properties(hostmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
  # specify the directory for the module compilation products
  pyre_library_directory(hostmodule extensions)
  # set the libraries to link against
  target_link_libraries(hostmodule PRIVATE pyre journal)
  # add the sources
  target_sources(hostmodule PRIVATE
    extensions/host/host.cc
    extensions/host/cpu.cc
    extensions/host/metadata.cc
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
  # if (Python_Development.Embed_FOUND)
  if (FALSE)
    # the pyre enhanced interpreter
    add_executable(python.pyre)
    # its sources
    target_sources(python.pyre PRIVATE
      bin/python.cc
      )
    # and libraries
    target_link_libraries(python.pyre Python::Python)

    # install the custom python
    install(
      TARGETS python.pyre
      RUNTIME
      DESTINATION ${CMAKE_INSTALL_BINDIR}
      )
  endif()
  # install the scripts
  install(
    PROGRAMS bin/pyre bin/pyre-config bin/merlin bin/smith.pyre
    DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
  # all done
endfunction(pyre_pyreBin)


# the configuration files
function(pyre_pyreDefaults)
  # install the configuration files
  install(
    DIRECTORY defaults/pyre defaults/merlin
    DESTINATION share
  )
  # all done
endfunction(pyre_pyreDefaults)


# generate a unique target name
function(pyre_target target testfile)
  # split
  get_filename_component(path ${testfile} DIRECTORY)
  get_filename_component(base ${testfile} NAME_WE)

  # replace path separators with dors
  string(REPLACE "/" "." stem ${path})

  # build the target and return it
  set(${target} "${stem}.${base}" PARENT_SCOPE)

  # all done
endfunction()


# specify the directory for the target compilation products
function(pyre_target_directory target directory)
  # set output directory for this target to subdirectory {directory} of the build directory
  set_target_properties(${target} PROPERTIES RUNTIME_OUTPUT_DIRECTORY
    ${CMAKE_CURRENT_BINARY_DIR}/${directory}
  )
# all done
endfunction()


# specify the directory for the module
function(pyre_library_directory library directory)
  # set output directory for this library to subdirectory {directory} of the build directory
  set_target_properties(${library} PROPERTIES LIBRARY_OUTPUT_DIRECTORY
    ${CMAKE_CURRENT_BINARY_DIR}/${directory}
  )
# all done
endfunction()


# add definitions to compilation of file
function(pyre_add_definitions driverfile)

  # the argument list is the list of definitions
  set(definitions ${ARGN})

  # generate the name of the target
  pyre_target(target ${driverfile})

  # for each definition requested
  foreach(definition IN LISTS definitions)
    # apply the definition to the target
    target_compile_definitions(${target} PRIVATE ${definition})
  endforeach()

# all done
endfunction()


# end of file
