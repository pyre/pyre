# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#


# register a benchmark case based on a compiled driver
function(pyre_benchmark_driver benchmarkfile)

  # generate the name of the target
  pyre_target(target ${benchmarkfile})

  # schedule it to be compiled
  add_executable(${target} ${benchmarkfile})
  # in release mode
  target_compile_options(${target} PRIVATE "-O3")
  # with some macros
  target_compile_definitions(${target} PRIVATE PYRE_CORE)
  # link against my libraries
  target_link_libraries(${target} PUBLIC pyre journal)
  # specify the directory for the target compilation products
  pyre_target_directory(${target} benchmarks)

  # all done
endfunction()


# register a benchmark case based on a compiled driver
function(pyre_benchmark_driver_cxx20 benchmarkfile)

  # generate the name of the target
  pyre_target(target ${benchmarkfile})

  # schedule it to be compiled
  add_executable(${target} ${benchmarkfile})
  # in release mode
  target_compile_options(${target} PRIVATE "-O3")
  # with some macros
  target_compile_definitions(${target} PRIVATE PYRE_CORE)
  # link against my libraries
  target_link_libraries(${target} PUBLIC pyre journal)
  # request c++20 to build the target
  target_compile_features(${target} PUBLIC cxx_std_20)
  target_compile_definitions(${target} PRIVATE WITH_CXX20)
  # specify the directory for the target compilation products
  pyre_target_directory(${target} benchmarks)

  # all done
endfunction()


# end of file
