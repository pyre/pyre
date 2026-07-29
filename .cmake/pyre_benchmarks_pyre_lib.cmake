# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# pyre
# tensor
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/matrix_plus_matrix.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/matrix_times_matrix.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/matrix_times_scalar.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/matrix_times_vector.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/matrix_norm.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/matrix_trace.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/matrix_determinant.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/vector_norm.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/vector_plus_vector.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/vector_scalar_product.cc)
pyre_benchmark_driver(benchmarks/pyre.lib/tensor/vector_times_scalar.cc)


# end of file
