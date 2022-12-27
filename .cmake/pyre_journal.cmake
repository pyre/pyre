# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# build the journal pcckage
function(pyre_journalPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY journal
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    journal/meta.py.in journal/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/journal
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(pyre_journalPackage)


# build libjournal
function(pyre_journalLib)
  # copy the journal headers over to the staging area
  file(GLOB_RECURSE files
       RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/journal
       CONFIGURE_DEPENDS
       *.h *.icc
       )
  foreach(file ${files})
    # skip the special header
    if("${file}" STREQUAL "journal.h")
      continue()
    endif()
    configure_file(journal/${file} pyre/journal/${file} COPYONLY)
  endforeach()

  # and the journal master header within the pyre directory
  configure_file(journal/journal.h pyre/journal.h COPYONLY)

  # the libjournal target
  add_library(journal SHARED)
  # define the core macro
  set_target_properties(journal PROPERTIES COMPILE_DEFINITIONS PYRE_CORE)
  # set the include directories
  target_include_directories(
    journal PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
    )
  # add the sources
  target_sources(journal
    PRIVATE
    journal/ANSI.cc
    journal/ANSI_x11.cc
    journal/Alert.cc
    journal/Bland.cc
    journal/Chronicler.cc
    journal/Console.cc
    journal/Device.cc
    journal/ErrorConsole.cc
    journal/File.cc
    journal/Memo.cc
    journal/Renderer.cc
    journal/Stream.cc
    journal/Trash.cc
    journal/debuginfo.cc
    journal/firewalls.cc
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
  # set the libraries to link against
  target_link_libraries(journalmodule PRIVATE journal pybind11::module)
  # add the sources
  target_sources(journalmodule PRIVATE
    journal/journal.cc
    journal/api.cc
    journal/chronicler.cc
    journal/debug.cc
    journal/devices.cc
    journal/entry.cc
    journal/error.cc
    journal/exceptions.cc
    journal/firewall.cc
    journal/help.cc
    journal/info.cc
    journal/warning.cc
    )
  # install
  install(
    TARGETS journalmodule
    LIBRARY
    DESTINATION ${PYRE_DEST_PACKAGES}/journal/ext
    )
endfunction(pyre_journalModule)


# end of file
