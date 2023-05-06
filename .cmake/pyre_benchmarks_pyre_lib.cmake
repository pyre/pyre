# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved
#


#
# pyre
#


# tensor
if (HAVE_TENSOR)
set(definitions "HAVE_TENSOR" "HAVE_COMPACT_PACKINGS")
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_plus_matrix.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/matrix_plus_matrix.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_times_matrix.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/matrix_times_matrix.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_times_scalar.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/matrix_times_scalar.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_times_vector.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/matrix_times_vector.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_trace.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/matrix_trace.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_determinant.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/matrix_determinant.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_norm.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/vector_norm.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_plus_vector.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/vector_plus_vector.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_scalar_product.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/vector_scalar_product.cc ${definitions})
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_times_scalar.cc)
pyre_add_definitions(benchmarks/pyre.lib/tensor/vector_times_scalar.cc ${definitions})
endif()


# end of file
