# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


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


# register a cuda parallel test case based on a compiled driver
function(pyre_benchmark_driver_cuda testfile)
  # create the name of the target
  pyre_target(target ${testfile})
  # create the object file for the corresponding cuda kernel
  pyre_kernel_target(kernelobject ${testfile})

  # schedule it to be compiled
  add_executable(${target} ${testfile})
  # with some macros
  target_compile_definitions(${target} PRIVATE PYRE_CORE WITH_CUDA)
  # link against my libraries
  target_link_libraries(${target} PUBLIC pyre journal cuda ${kernelobject})

  # specify the directory for the target compilation products
  pyre_target_directory(${target} benchmarks)

  # all done
endfunction()


# end of file
