# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2020 all rights reserved
#

# cmake setup
cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
# policies
if (POLICY CMP0048)
  cmake_policy(SET CMP0048 NEW)
endif(POLICY CMP0048)
cmake_policy(SET CMP0060 NEW)
if (POLICY CMP0074)
  cmake_policy(SET CMP0074 NEW)
endif(POLICY CMP0074)
if (POLICY CMP0076)
  cmake_policy(SET CMP0076 NEW)
endif(POLICY CMP0076)

# options
option(WITH_CUDA "enable support for CUDA" OFF)

# adjust the include path
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/.cmake)
# get support
include(pyre_init)
include(pyre_journal)
include(pyre_pyre)
include(pyre_merlin)
include(pyre_cuda)
include(pyre_mpi)
include(pyre_gsl)
include(pyre_postgres)

# ask git for the pyre version
pyre_getVersion()

# set up the project
project(PYRE VERSION ${REPO_MAJOR}.${REPO_MINOR}.${REPO_MICRO} LANGUAGES CXX C)
# hmmmm
include(GNUInstallDirs)

# programs
find_program(BASH_PROGRAM bash)

# packages
# gsl
find_package(GSL)
# mpi
find_package(MPI)
# postgres
find_package(PostgreSQL)
# python
find_package(Python3 COMPONENTS Interpreter Development NumPy)

# set up cmake
pyre_cmakeInit()
# set up c++
pyre_cxxInit()
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

# install config file for find_package
include(CMakePackageConfigHelpers)
configure_package_config_file(
    ${PROJECT_SOURCE_DIR}/.cmake/pyre-config.cmake.in
    ${PROJECT_BINARY_DIR}/pyre-config.cmake
    INSTALL_DESTINATION ${PYRE_CMAKE_DIR})
install(FILES ${PROJECT_BINARY_DIR}/pyre-config.cmake
        DESTINATION ${PYRE_CMAKE_DIR})

# create aliases matching the exports above
add_library(pyre::pyre    ALIAS pyre)
add_library(pyre::journal ALIAS journal)


# if we are building to test
if(BUILD_TESTING)
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
