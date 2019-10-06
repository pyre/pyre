# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# setup cmake
function(pyre_cmakeInit)
  # get the source directory
  get_filename_component(srcdir "${CMAKE_SOURCE_DIR}" REALPATH)
  # get the staging directory
  get_filename_component(stgdir "${CMAKE_BINARY_DIR}" REALPATH)
  # if we are building within the source directory
  if ("${srcdir}" STREQUAL "${stgdir}")
    # complain and bail
    message(FATAL_ERROR "in-source build detected; please run cmake in a build directory")
  endif()

  # quiet install
  set(CMAKE_INSTALL_MESSAGE LAZY PARENT_SCOPE)

  # if the user asked for CUDA support
  if (WITH_CUDA)
    # turn it on
    enable_language(CUDA)
  endif()

  # all done
endfunction(pyre_cmakeInit)


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
  set(PYRE_DEST_PACKAGES packages PARENT_SCOPE)
  # all done
endfunction(pyre_destinationInit)


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
  set(GIT_DESCRIBE "v([0-9]+)\\.([0-9]+)\\.([0-9]+)-([0-9]+)-g(.+)" )
  # parse the bits
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\1" REPO_MAJOR ${GIT_DESCRIBE_VERSION} )
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\2" REPO_MINOR ${GIT_DESCRIBE_VERSION})
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\3" REPO_MICRO ${GIT_DESCRIBE_VERSION})
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\5" REPO_COMMIT ${GIT_DESCRIBE_VERSION})

  # export our local variables
  set(REPO_MAJOR ${REPO_MAJOR} PARENT_SCOPE)
  set(REPO_MINOR ${REPO_MINOR} PARENT_SCOPE)
  set(REPO_MICRO ${REPO_MICRO} PARENT_SCOPE)
  set(REPO_COMMIT ${REPO_COMMIT} PARENT_SCOPE)

  # all done
endfunction(pyre_getVersion)


# end of file
