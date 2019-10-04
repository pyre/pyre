# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# git
find_package(git REQUIRED)
# get tag info
execute_process(
  COMMAND ${GIT_EXECUTABLE} describe --tags --long --always
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  RESULT_VARIABLE GIT_DESCRIBE_STATUS
  OUTPUT_VARIABLE GIT_DESCRIBE_VERSION
  OUTPUT_STRIP_TRAILING_WHITESPACE
  )

# the parser of the "git describe" result
set(GIT_DESCRIBE "v([0-9]+)\\.([0-9]+)\\.([0-9]+)-([0-9])-(.+)" )
# parse the bits
string(REGEX REPLACE ${GIT_DESCRIBE} "\\1" PYRE_MAJOR ${GIT_DESCRIBE_VERSION} )
string(REGEX REPLACE ${GIT_DESCRIBE} "\\2" PYRE_MINOR ${GIT_DESCRIBE_VERSION})
string(REGEX REPLACE ${GIT_DESCRIBE} "\\3" PYRE_MICRO ${GIT_DESCRIBE_VERSION})
string(REGEX REPLACE ${GIT_DESCRIBE} "\\5" PYRE_HASH ${GIT_DESCRIBE_VERSION})

# end of file
