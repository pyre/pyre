# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a mock downstream project
# it exists to exercise the {pyre} package configuration the way a real client does: from the
# outside, against an installed prefix, with nothing but {find_package} to go on; it is never
# built as part of {pyre} itself
cmake_minimum_required(VERSION 3.20)
project(pyre-consumer LANGUAGES CXX)

# what the installation under test is expected to carry
option(PYRE_CONSUMER_EXPECT_HDF5 "the installation was built against hdf5" OFF)
option(PYRE_CONSUMER_EXPECT_MPI "the installation carries the mpi add-on" OFF)
option(PYRE_CONSUMER_EXPECT_CUDA "the installation carries the cuda add-on" OFF)

# deliberately, there is no {find_package(HDF5)} or {find_package(MPI)} ahead of this call, and
# no {CMAKE_CXX_STANDARD} anywhere in this file: resolving the dependencies of the exported
# targets and raising the language standard are the package configuration's job, and whether it
# does them is precisely what this project tests
# note also that this comes before any {add_executable} below, which is what lets the
# configuration turn the compiler extensions off for our targets; a project that declares its
# targets first would quietly get {gnu++23} instead
find_package(pyre REQUIRED)

# the export set: these are the two targets the package promises
foreach(target pyre::pyre pyre::journal)
  # each of them must have made it out of the targets file
  if(NOT TARGET ${target})
    # if not, the installation is unusable
    message(FATAL_ERROR "the {pyre} package did not define '${target}'")
  endif()
endforeach()

# the core pieces announce themselves as components, so that {find_package(pyre COMPONENTS ...)}
# can be answered; check the two that are always there
foreach(component pyre journal)
  # each must have been published by the configuration
  if(NOT pyre_${component}_FOUND)
    message(FATAL_ERROR "the {pyre} package did not publish the '${component}' component")
  endif()
endforeach()

# the optional add-ons ship only when the build found what they wrap; whenever one is announced,
# the target that goes with it has to be there too, or the announcement is a lie
foreach(component mpi postgres cuda)
  # an add-on this installation does not carry is not a problem
  if(pyre_${component}_FOUND AND NOT TARGET pyre::${component})
    message(FATAL_ERROR "the {pyre} package announced '${component}' but defined no target")
  endif()
endforeach()

# the version file must have told us what we found
if(NOT pyre_VERSION)
  # otherwise {find_package(pyre 2.0)} would have nothing to compare against
  message(FATAL_ERROR "the {pyre} package did not report a version")
endif()

# the standard must have arrived as a usage requirement, without extensions
if(CMAKE_CXX_EXTENSIONS)
  # a consumer that gets {gnu++23} is not getting what our headers were written against
  message(FATAL_ERROR "the {pyre} package left the compiler extensions turned on")
endif()

# now check the exported link interface against what this installation was built with; asking
# about the interface rather than about the global target namespace matters, because a bare
# {if(TARGET HDF5::HDF5)} would pass for the wrong reason the moment anything else finds hdf5
get_target_property(interface pyre::pyre INTERFACE_LINK_LIBRARIES)
# if hdf5 was in the build
if(PYRE_CONSUMER_EXPECT_HDF5)
  # the wrappers must be in the interface
  if(NOT "HDF5::HDF5" IN_LIST interface)
    message(FATAL_ERROR "'pyre::pyre' does not carry HDF5::HDF5 in its link interface")
  endif()
  # and the configuration must have resolved it on our behalf
  if(NOT TARGET HDF5::HDF5)
    message(FATAL_ERROR "the {pyre} package did not locate hdf5 for us")
  endif()
# otherwise
else()
  # nothing in the interface may demand it
  if("HDF5::HDF5" IN_LIST interface)
    message(FATAL_ERROR "'pyre::pyre' demands HDF5::HDF5 from an installation built without it")
  endif()
endif()

# the drivers get run, not just built: unresolved symbols, the {libpyre} to {libjournal} lookup
# at load time, and headers that disagree with the library they were installed next to are all
# invisible to a compile-only check
enable_testing()

# journal on its own
add_executable(journal journal.cc)
# it links against nothing else
target_link_libraries(journal PRIVATE pyre::journal)
# and it must run cleanly
add_test(NAME journal COMMAND journal)

# libpyre; note that we never name {pyre::journal} here, so this also checks that it arrives
# transitively through the exported interface
add_executable(pyre pyre.cc)
# the one link a client should need
target_link_libraries(pyre PRIVATE pyre::pyre)
# and it must run cleanly
add_test(NAME pyre COMMAND pyre)

# the mpi add-on, when this installation has it; asking for it by name is what makes the
# configuration go looking for mpi, which it deliberately does not do for consumers who never
# mention the component
if(PYRE_CONSUMER_EXPECT_MPI)
  # this second call re-runs the configuration, this time with a component list
  find_package(pyre REQUIRED COMPONENTS mpi)
  # which must have resolved the imported target the add-on names
  if(NOT TARGET MPI::MPI_CXX)
    message(FATAL_ERROR "asking for the 'mpi' component did not locate mpi")
  endif()
  # compiling this proves the mpi headers arrive through {pyre::mpi}
  add_executable(mpi mpi.cc)
  # the one link a client should need
  target_link_libraries(mpi PRIVATE pyre::mpi)
  # and it must run cleanly
  add_test(NAME mpi COMMAND mpi)
endif()

# the cuda add-on, on the same terms as mpi above
if(PYRE_CONSUMER_EXPECT_CUDA)
  # asking for the component is what sends the configuration looking for what it needs
  find_package(pyre REQUIRED COMPONENTS cuda)
  # the deprecated {FindCUDA} builds its library list out of the threads imported target, so
  # that is the one the add-on leans on
  if(NOT TARGET Threads::Threads)
    message(FATAL_ERROR "asking for the 'cuda' component did not locate threads")
  endif()
  # compiling this proves the cuda headers and our own arrive through {pyre::cuda}
  add_executable(cuda cuda.cc)
  # the one link a client should need
  target_link_libraries(cuda PRIVATE pyre::cuda)
  # and it must run cleanly
  add_test(NAME cuda COMMAND cuda)
endif()

# the hdf5 wrappers, when this installation has them
if(PYRE_CONSUMER_EXPECT_HDF5)
  # compiling this at all proves the hdf5 headers arrive through {pyre::pyre}
  add_executable(h5 h5.cc)
  # again, the single link
  target_link_libraries(h5 PRIVATE pyre::pyre)
  # and it must run cleanly
  add_test(NAME h5 COMMAND h5)
endif()


# end of file
