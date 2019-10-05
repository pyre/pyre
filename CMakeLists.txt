# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# cmake setup
cmake_minimum_required(VERSION 3.11 FATAL_ERROR)
# policies
if (POLICY CMP0048)
  cmake_policy(SET CMP0048 NEW)
endif (POLICY CMP0048)
cmake_policy(SET CMP0060 NEW)
if (POLICY CMP0074)
  cmake_policy(SET CMP0074 NEW)
endif(POLICY CMP0074)

# adjust the include path
list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/.cmake)

# get support
include(pyre)
# ask git for the pyre version
pyre_getVersion()

# set up the project
project(PYRE VERSION ${PYRE_MAJOR}.${PYRE_MINOR}.${PYRE_MICRO} LANGUAGES CXX)
# show me
message("++ pyre version: ${PYRE_MAJOR}.${PYRE_MINOR}.${PYRE_MICRO} build ${PYRE_HASH}")


# set up c++
pyre_cxxInit()
# set up python
pyre_pythonInit()

# initialize the variables that describe the staging directory layout
pyre_stagingInit()
# initialize the variables that describe the install directory layout
pyre_destinationInit()

# visit subdirectories
#add_subdirectory(packages)


# end of file
