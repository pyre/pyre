# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# build the survey package
function(pyre_surveyPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY packages/survey
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    packages/survey/meta.py.in packages/survey/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/packages/survey
    DESTINATION ${PYRE_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(pyre_surveyPackage)


# end of file
