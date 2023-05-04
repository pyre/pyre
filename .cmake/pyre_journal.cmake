# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2020 all rights reserved
#


# buld the journal pcckage
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
  file(
    COPY journal
    DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/pyre
    FILES_MATCHING
    PATTERN *.h PATTERN *.icc
    PATTERN journal/journal.h EXCLUDE
    )
  # and the journal master header within the pyre directory
  file(
    COPY journal/journal.h
    DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/pyre
    )

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
    journal/Chronicler.cc
    journal/Console.cc
    journal/Device.cc
    journal/ErrorConsole.cc
    journal/File.cc
    journal/Memo.cc
    journal/Renderer.cc
    journal/Splitter.cc
    journal/Stream.cc
    journal/Trash.cc
    journal/debuginfo.cc
    journal/firewalls.cc
    )
  target_link_libraries(journal PUBLIC std::filesystem)

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
  Python3_add_library(journalmodule MODULE)
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
    journal/error.cc
    journal/exceptions.cc
    journal/firewall.cc
    journal/info.cc
    journal/opaque.cc
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
