# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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

  # host info
  # get
  string(TOLOWER ${CMAKE_HOST_SYSTEM_NAME} HOST_OS)
  string(TOLOWER ${CMAKE_HOST_SYSTEM_PROCESSOR} HOST_ARCH)
  # export
  set(HOST_OS ${HOST_OS} PARENT_SCOPE)
  set(HOST_ARCH ${HOST_ARCH} PARENT_SCOPE)
  set(HOST_PLATFORM ${HOST_OS}_${HOST_ARCH} PARENT_SCOPE)

  # quiet install
  set(CMAKE_INSTALL_MESSAGE LAZY PARENT_SCOPE)

  # if the user asked for CUDA support
  if (WITH_CUDA)
    # turn it on
    enable_language(CUDA)
  endif()

  # all done
endfunction(pyre_cmakeInit)


# setup python
function(pyre_pythonInit)
  # ask the executable for the module suffix
  execute_process(
    COMMAND ${Python_EXECUTABLE} -c
        "from distutils.sysconfig import *; print(get_config_var('EXT_SUFFIX'))"
    RESULT_VARIABLE PYTHON3_SUFFIX_STATUS
    OUTPUT_VARIABLE PYTHON3_SUFFIX
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )
  # export
  set(PYTHON3_SUFFIX ${PYTHON3_SUFFIX} PARENT_SCOPE)
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
  set(PYRE_DEST_INCLUDE ${CMAKE_INSTALL_INCLUDEDIR} PARENT_SCOPE)
  if(NOT DEFINED PYRE_DEST_PACKAGES)
      set(PYRE_DEST_PACKAGES packages CACHE STRING
          "Python package install location, absolute or relative to install prefix")
  endif()
  # Translate to unconditional absolute path
  get_filename_component(PYRE_DEST_FULL_PACKAGES ${PYRE_DEST_PACKAGES} ABSOLUTE
                         BASE_DIR ${CMAKE_INSTALL_PREFIX})
  set(PYRE_DEST_FULL_PACKAGES ${PYRE_DEST_FULL_PACKAGES} PARENT_SCOPE)
  # all done
endfunction(pyre_destinationInit)


# describe the root pf tyhe test suite
function(pyre_testInit)
  # create a variable to hold the root in the test directory
  set(PYRE_TESTSUITE_DIR ${CMAKE_SOURCE_DIR}/tests PARENT_SCOPE)
  set(PYRE_TESTSUITE_TMPDIR ${CMAKE_BINARY_DIR}/tmp PARENT_SCOPE)
  # all done
endfunction(pyre_testInit)


# ask git for the most recent tag and use it to build the version
function(pyre_getVersion)
  # git
  find_package(Git REQUIRED)
  # get tag info
  execute_process(
    COMMAND ${GIT_EXECUTABLE} describe --tags --long --always
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE GIT_DESCRIBE_STATUS
    OUTPUT_VARIABLE GIT_DESCRIBE_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )
  if(NOT "${GIT_DESCRIBE_STATUS}" STREQUAL "0")
    message(FATAL_ERROR "git describe --tags --long --always failed")
  endif()

  set(GIT_DESCRIBE "v([0-9]+)\\.([0-9]+)\\.([0-9]+)-([0-9]+)-g(.+)" )
  if(NOT GIT_DESCRIBE_VERSION MATCHES ${GIT_DESCRIBE})
    message(FATAL_ERROR "Invalid version string: ${GIT_DESCRIBE_VERSION}")
  endif()

  # parse the bits
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\1" REPO_MAJOR ${GIT_DESCRIBE_VERSION} )
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\2" REPO_MINOR ${GIT_DESCRIBE_VERSION})
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\3" REPO_MICRO ${GIT_DESCRIBE_VERSION})
  string(REGEX REPLACE ${GIT_DESCRIBE} "\\5" REPO_COMMIT ${GIT_DESCRIBE_VERSION})

  set(PYRE_VERSION "${REPO_MAJOR}.${REPO_MINOR}.${REPO_MICRO}" PARENT_SCOPE)
  set(REVISION ${REPO_COMMIT} PARENT_SCOPE)
  string(TIMESTAMP TODAY PARENT_SCOPE)

  # all done
endfunction(pyre_getVersion)


# end of file
