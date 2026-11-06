# -*- cmake -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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

  # all done
endfunction(pyre_cmakeInit)


# setup python
function(pyre_pythonInit)
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
  set(PYRE_DEST_SHARE ${CMAKE_INSTALL_PREFIX}/share PARENT_SCOPE)
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


# install a binary in {destination}, absolute or relative to the prefix, and teach it where to
# find our libraries: by a path relative to its own location when the binary and the libraries
# both live in the prefix, so the prefix keeps working wherever it is moved, and by the place the
# libraries are installed in otherwise; a binary that consumers can ask for by name names its
# export set after the EXPORT keyword
function(pyre_installBinary target destination)
  # collect the export set, if any
  cmake_parse_arguments(PARSE_ARGV 2 binary "" "EXPORT" "")
  # programs go where programs are installed, and everything else is a library
  get_target_property(type ${target} TYPE)
  if(type STREQUAL "EXECUTABLE")
    set(kind RUNTIME)
  else()
    set(kind LIBRARY)
  endif()
  # add the binary to its export set, when it has one
  set(exports "")
  if(DEFINED binary_EXPORT)
    set(exports EXPORT ${binary_EXPORT})
  endif()
  # install it
  install(TARGETS ${target} ${exports} ${kind} DESTINATION ${destination})

  # find the directory the binary is installed in
  cmake_path(ABSOLUTE_PATH destination BASE_DIRECTORY "${CMAKE_INSTALL_PREFIX}" NORMALIZE
             OUTPUT_VARIABLE home)
  # a relative path survives a move only when both ends of it move with the prefix
  cmake_path(IS_PREFIX CMAKE_INSTALL_PREFIX "${home}" NORMALIZE homeMoves)
  cmake_path(IS_PREFIX CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_FULL_LIBDIR}" NORMALIZE
             librariesMove)
  # when either one lives elsewhere, the installation cannot be moved anyway
  if(NOT (homeMoves AND librariesMove))
    # so the binary looks for our libraries where they are installed
    set_target_properties(${target} PROPERTIES INSTALL_RPATH "${CMAKE_INSTALL_FULL_LIBDIR}")
    # and we are done
    return()
  endif()
  # otherwise, find the way from the binary to our libraries
  set(libraries "${CMAKE_INSTALL_FULL_LIBDIR}")
  cmake_path(RELATIVE_PATH libraries BASE_DIRECTORY "${home}" OUTPUT_VARIABLE path)
  # the loader has its own name for the directory of the binary on each platform
  if(APPLE)
    set(origin "@loader_path")
  else()
    set(origin "$ORIGIN")
  endif()
  # a binary that lives next to our libraries needs only its own directory
  if(path STREQUAL ".")
    set(rpath "${origin}")
  # everything else walks over to them
  else()
    set(rpath "${origin}/${path}")
  endif()
  # record the path with the target
  set_target_properties(${target} PROPERTIES INSTALL_RPATH "${rpath}")
  # all done
endfunction(pyre_installBinary)


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

  # all done
endfunction(pyre_getVersion)


# find the revision of the source when the caller supplies the version
function(pyre_getRevision)
  # a clone knows its own revision
  if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/.git)
    # so, if git is around
    find_package(Git)
    if(Git_FOUND)
      # ask it for the commit that is checked out, abbreviated the way {git describe} does
      execute_process(
        COMMAND ${GIT_EXECUTABLE} rev-parse --short=9 HEAD
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        RESULT_VARIABLE GIT_REVPARSE_STATUS
        OUTPUT_VARIABLE GIT_REVPARSE_COMMIT
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
        )
      # and use it, if it answered
      if("${GIT_REVPARSE_STATUS}" STREQUAL "0")
        set(REVISION ${GIT_REVPARSE_COMMIT} PARENT_SCOPE)
        return()
      endif()
    endif()
  endif()

  # a tarball made by {git archive} carries the commit in its archival record, where git
  # has filled in the placeholder on the way out
  set(ARCHIVAL ${CMAKE_CURRENT_SOURCE_DIR}/.git_archival.txt)
  if(EXISTS ${ARCHIVAL})
    # look for the commit
    file(STRINGS ${ARCHIVAL} ARCHIVAL_NODE REGEX "^node: [0-9a-f]+$")
    # and, if it is there, abbreviate it the same way
    if(ARCHIVAL_NODE)
      string(REGEX REPLACE "^node: ([0-9a-f]+)$" "\\1" ARCHIVAL_COMMIT "${ARCHIVAL_NODE}")
      string(SUBSTRING ${ARCHIVAL_COMMIT} 0 9 ARCHIVAL_COMMIT)
      set(REVISION ${ARCHIVAL_COMMIT} PARENT_SCOPE)
      return()
    endif()
  endif()

  # otherwise, the revision is unknown
  set(REVISION "" PARENT_SCOPE)
  # all done
endfunction(pyre_getRevision)


# end of file
