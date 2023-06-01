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

  # all done
endfunction()


# end of file
