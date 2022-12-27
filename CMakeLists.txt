# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

# cmake setup
cmake_minimum_required(VERSION 3.12...3.18)

# options
option(WITH_CUDA "enable support for CUDA" OFF)

# adjust the include path
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/.cmake)
# get support
include(pyre_init)

if(NOT PYRE_VERSION)
    if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/.git)
        message(FATAL_ERROR "git auto-versioning requires cloned repo! "
                            "provide a version with -DPYRE_VERSION=X.Y.Z")
    endif()

    # ask git for the pyre version
    pyre_getVersion()
endif()

# set up the project
project(PYRE VERSION "${PYRE_VERSION}" LANGUAGES CXX)
set(MAJOR ${PROJECT_VERSION_MAJOR})
set(MINOR ${PROJECT_VERSION_MINOR})
set(MICRO ${PROJECT_VERSION_PATCH})

# is this the topmost project? (not added via e.g. add_subdirectory)
if(PROJECT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  set(PYRE_IS_ROOT_PROJECT TRUE)
else()
  set(PYRE_IS_ROOT_PROJECT FALSE)
endif()

# default to build tests only when root project, but allow user to choose
option(PYRE_BUILD_TESTING "Build pyre's test suite" ${PYRE_IS_ROOT_PROJECT})

# hmmmmm
include(GNUInstallDirs)

# RPATH handling
# https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/RPATH-handling
# use, i.e. don't skip the full RPATH for the build tree
set(CMAKE_SKIP_BUILD_RPATH FALSE)

# when building, don't use the install RPATH already
# (but later on when installing)
set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_FULL_LIBDIR}")

# add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# the RPATH to be used when installing, but only if it's not a system directory
if(NOT (CMAKE_INSTALL_FULL_LIBDIR IN_LIST
        CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES))
    set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_FULL_LIBDIR}")
endif()

include(pyre_journal)
include(pyre_pyre)
include(pyre_merlin)
include(pyre_cuda)
include(pyre_mpi)
include(pyre_gsl)
include(pyre_h5)
include(pyre_postgres)

# programs
find_program(BASH_PROGRAM bash)

# packages
# mpi; esrly so packages that depend on it know
find_package(MPI COMPONENTS CXX)

# gsl
find_package(GSL)

# hdf5
# if mpi is installed
if(${MPI_FOUND})
    # prefer the parallel version of hdf5
    set(HDF5_PREFER_PARALLEL ON)
endif()
message("parallel hdf5: ${HDF5_PREFER_PARALLEL}")
# hunt it down
find_package(HDF5 COMPONENTS CXX HL)

# postgres
find_package(PostgreSQL)

# python
find_package(Python 3.7 COMPONENTS Interpreter Development NumPy)

# for building bindings
# require c++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(PYBIND11_CPP_STANDARD -std=c++17)
set(PYBIND11_PYTHON_VERSION ${Python_VERSION})
set(PYBIND11_FINDPYTHON ON) # Use new FindPython if available
find_package(pybind11)

# pybind11 pre-2.5 C++17 compilation is broken under Clang
# see https://github.com/pybind/pybind11/issues/1604#issuecomment-443385783
if(pybind11_VERSION VERSION_LESS 2.5 AND CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(pybind11::module INTERFACE -fsized-deallocation)
endif()

# set up cmake
pyre_cmakeInit()
# set up python
pyre_pythonInit()

# initialize the variables that describe the staging directory layout
pyre_stagingInit()
# initialize the variables that describe the install directory layout
pyre_destinationInit()

# visit subdirectories
add_subdirectory(packages)
add_subdirectory(lib)
add_subdirectory(extensions)
add_subdirectory(defaults)
add_subdirectory(bin)

# make exports available in binary dir during build
export(EXPORT pyre-targets
       NAMESPACE pyre::
       )

# install exports to installation prefix
set(PYRE_CMAKE_DIR "share/cmake/pyre" CACHE STRING
    "Installation directory for cmake files, relative to install prefix")
install(EXPORT pyre-targets
        NAMESPACE pyre::
        DESTINATION ${PYRE_CMAKE_DIR}
        )

# set up version detection for cmake find_package
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    pyre-config-version.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMinorVersion
    )

# install config file for find_package
configure_package_config_file(
    ${PROJECT_SOURCE_DIR}/.cmake/pyre-config.cmake.in
    ${PROJECT_BINARY_DIR}/pyre-config.cmake
    INSTALL_DESTINATION ${PYRE_CMAKE_DIR})
install(FILES ${PROJECT_BINARY_DIR}/pyre-config.cmake
              ${PROJECT_BINARY_DIR}/pyre-config-version.cmake
        DESTINATION ${PYRE_CMAKE_DIR})

# create aliases matching the exports above
add_library(pyre::pyre    ALIAS pyre)
add_library(pyre::journal ALIAS journal)


# if we are building to test
if(PYRE_BUILD_TESTING)

  # needed by some {journal} test cases
  enable_language(C)

  # get support
  include(CTest)
  # and my functions
  include(pyre_tests)

  # initialize the variables that describe the test suite; needed so harnesses can set up the
  # working directory correctly
  pyre_testInit()
  # add the testsuite to the pile
  add_subdirectory(tests)
endif()


# end of file
