# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# ask git for the most recent tag and use it to build the version
function(pyre_getVersion)
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
  set(GIT_DESCRIBE "v([0-9]+)\\.([0-9]+)\\.([0-9]+)-([0-9])-g(.+)" )
  # parse the bits
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\1" PYRE_MAJOR ${GIT_DESCRIBE_VERSION} )
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\2" PYRE_MINOR ${GIT_DESCRIBE_VERSION})
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\3" PYRE_MICRO ${GIT_DESCRIBE_VERSION})
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\5" PYRE_HASH ${GIT_DESCRIBE_VERSION})

  # export our local variables
  set(PYRE_MAJOR ${PYRE_MAJOR} PARENT_SCOPE)
  set(PYRE_MINOR ${PYRE_MINOR} PARENT_SCOPE)
  set(PYRE_MICRO ${PYRE_MICRO} PARENT_SCOPE)
  set(PYRE_HASH  ${PYRE_HASH} PARENT_SCOPE)

  # all done
endfunction(pyre_getVersion)


# setup the c++ compiler
function(pyre_cxxInit)
  # require c++17
  set(CMAKE_CXX_STANDARD 17 PARENT_SCOPE)
  set(CMAKE_CXX_STANDARD_REQUIRED ON PARENT_SCOPE)
  set(CMAKE_CXX_EXTENSIONS OFF PARENT_SCOPE)
  # all done
endfunction(pyre_cxxInit)


# setup python
function(pyre_pythonInit)
  # get the interpreter
  find_package(Python3 COMPONENTS Interpreter Development NumPy)
  # all done
endfunction(pyre_pythonInit)


# describe the layout of the staging area
function(pyre_stagingInit)
  # the layout
  set(PYRE_STAGING_PACKAGES ${CMAKE_BINARY_DIR}/packages PARENT_SCOPE)
  # all done
endfunction(pyre_stagingInit)


# describe the installation layout
function(pyre_destinationInit)
  # create variables to hold the roots in the install directory
  set(PYRE_DEST_PACAKGES packages PARENT_SCOPE)
  # all done
endfunction(pyre_destinationInit)


# end of file
