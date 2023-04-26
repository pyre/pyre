# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#


# generate a unique benchmark target name
function(pyre_benchmark_target target testfile)
  # split
  get_filename_component(path ${testfile} DIRECTORY)
  get_filename_component(base ${testfile} NAME_WE)

  # replace path separators with dors
  string(REPLACE "/" "." stem ${path})

  # build the target and return it
  set(${target} "benchmarks.${stem}.${base}" PARENT_SCOPE)

  # all done
endfunction()


# register a benchmark case based on a compiled driver
function(pyre_benchmark_driver_cxx20 benchmarkfile)

  # generate the name of the target
  pyre_benchmark_target(target ${benchmarkfile})

  # schedule it to be compiled
  add_executable(${target} ${benchmarkfile})
  # in release mode
  target_compile_options(${target} PRIVATE $<$<CONFIG:Release>:-O3>)
  # with some macros
  target_compile_definitions(${target} PRIVATE PYRE_CORE)
  target_compile_definitions(${target} PRIVATE HAVE_COMPACT_PACKINGS)
  # link against my libraries
  target_link_libraries(${target} PUBLIC pyre journal)
  # request c++20 to build the target
  target_compile_features(${target} PUBLIC cxx_std_20)
  target_compile_definitions(${target} PRIVATE WITH_CXX20)

  # all done
endfunction()


# end of file
