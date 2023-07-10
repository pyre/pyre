# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# build the journal package
function(pyre_journalPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY packages/journal
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    packages/journal/meta.py.in packages/journal/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/packages/journal
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(pyre_journalPackage)


# build libjournal
function(pyre_journalLib)
  # copy the journal headers over to the staging area
  file(GLOB_RECURSE files
       RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/lib/journal
       CONFIGURE_DEPENDS
       lib/journal/*.h lib/journal/*.icc
       )
  foreach(file ${files})
    # skip the special header
    if("${file}" STREQUAL "journal.h")
      continue()
    endif()
    configure_file(lib/journal/${file} lib/pyre/journal/${file} COPYONLY)
  endforeach()

  # and the journal master header within the pyre directory
  configure_file(lib/journal/journal.h lib/pyre/journal.h COPYONLY)

  # the libjournal target
  add_library(journal SHARED)
  # specify the directory for the library compilation products
  pyre_library_directory(journal lib)
  # define the core macro
  set_target_properties(journal PROPERTIES COMPILE_DEFINITIONS PYRE_CORE)
  # set the include directories
  target_include_directories(
    journal PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/lib>
    $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
    )
  # add the sources
  target_sources(journal
    PRIVATE
    lib/journal/ANSI.cc
    lib/journal/ANSI_x11.cc
    lib/journal/Alert.cc
    lib/journal/Bland.cc
    lib/journal/Chronicler.cc
    lib/journal/Console.cc
    lib/journal/Device.cc
    lib/journal/ErrorConsole.cc
    lib/journal/File.cc
    lib/journal/Memo.cc
    lib/journal/Renderer.cc
    lib/journal/Stream.cc
    lib/journal/Trash.cc
    lib/journal/debuginfo.cc
    lib/journal/firewalls.cc
    )

  # libpyre and libjournal
  install(
    TARGETS journal
    EXPORT pyre-targets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )

  # all done
endfunction(pyre_journalLib)


# build the journal python extension
function(pyre_journalModule)
  # journal
  Python_add_library(journalmodule MODULE)
  # turn on the core macro
  set_target_properties(journalmodule PROPERTIES COMPILE_DEFINITIONS PYRE_CORE)
  # adjust the name to match what python expects
  set_target_properties(journalmodule PROPERTIES LIBRARY_OUTPUT_NAME journal)
  set_target_properties(journalmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
  # specify the directory for the module compilation products
  pyre_library_directory(journalmodule extensions)
  # set the libraries to link against
  target_link_libraries(journalmodule PRIVATE journal pybind11::module)
  # add the sources
  target_sources(journalmodule PRIVATE
    extensions/journal/journal.cc
    extensions/journal/api.cc
    extensions/journal/chronicler.cc
    extensions/journal/debug.cc
    extensions/journal/devices.cc
    extensions/journal/entry.cc
    extensions/journal/error.cc
    extensions/journal/exceptions.cc
    extensions/journal/firewall.cc
    extensions/journal/help.cc
    extensions/journal/info.cc
    extensions/journal/warning.cc
    )
  # install
  install(
    TARGETS journalmodule
    LIBRARY
    DESTINATION ${PYRE_DEST_PACKAGES}/journal/ext
    )
endfunction(pyre_journalModule)


# end of file
