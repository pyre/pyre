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
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_plus_matrix.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_times_matrix.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_times_scalar.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_times_vector.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/matrix_determinant.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_norm.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_plus_vector.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_scalar_product.cc)
pyre_benchmark_driver_cxx20(benchmarks/pyre.lib/tensor/vector_times_scalar.cc)
endif()


# end of file
