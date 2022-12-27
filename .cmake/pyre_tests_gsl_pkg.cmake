# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

#
# gsl
#
# sanity
pyre_test_python_testcase(gsl.pkg/sanity.py)
# general
pyre_test_python_testcase(gsl.pkg/rng.py)
pyre_test_python_testcase(gsl.pkg/pdf.py)
pyre_test_python_testcase(gsl.pkg/permutation.py)
pyre_test_python_testcase(gsl.pkg/vector.py)
pyre_test_python_testcase(gsl.pkg/matrix.py)
pyre_test_python_testcase(gsl.pkg/blas.py)
pyre_test_python_testcase(gsl.pkg/linalg.py)
# random numbers
pyre_test_python_testcase(gsl.pkg/rng_available.py)
pyre_test_python_testcase(gsl.pkg/rng_allocate.py)
pyre_test_python_testcase(gsl.pkg/rng_range.py)
pyre_test_python_testcase(gsl.pkg/rng_int.py)
pyre_test_python_testcase(gsl.pkg/rng_float.py)
# pdfs
pyre_test_python_testcase(gsl.pkg/pdf_uniform.py)
pyre_test_python_testcase(gsl.pkg/pdf_uniform_pos.py)
pyre_test_python_testcase(gsl.pkg/pdf_gaussian.py)
pyre_test_python_testcase(gsl.pkg/pdf_dirichlet.py)
# permutations
pyre_test_python_testcase(gsl.pkg/permutation_allocate.py)
pyre_test_python_testcase(gsl.pkg/permutation_copy.py)
pyre_test_python_testcase(gsl.pkg/permutation_get.py)
# vectors
pyre_test_python_testcase(gsl.pkg/vector_allocate.py)
pyre_test_python_testcase(gsl.pkg/vector_zero.py)
pyre_test_python_testcase(gsl.pkg/vector_fill.py)
pyre_test_python_testcase(gsl.pkg/vector_random.py)
pyre_test_python_testcase(gsl.pkg/vector_clone.py)
pyre_test_python_testcase(gsl.pkg/vector_set.py)
pyre_test_python_testcase(gsl.pkg/vector_slices.py)
pyre_test_python_testcase(gsl.pkg/vector_contains.py)
pyre_test_python_testcase(gsl.pkg/vector_tuple.py)
pyre_test_python_testcase(gsl.pkg/vector_add.py)
pyre_test_python_testcase(gsl.pkg/vector_sub.py)
pyre_test_python_testcase(gsl.pkg/vector_mul.py)
pyre_test_python_testcase(gsl.pkg/vector_div.py)
pyre_test_python_testcase(gsl.pkg/vector_shift.py)
pyre_test_python_testcase(gsl.pkg/vector_scale.py)
pyre_test_python_testcase(gsl.pkg/vector_max.py)
pyre_test_python_testcase(gsl.pkg/vector_min.py)
pyre_test_python_testcase(gsl.pkg/vector_minmax.py)
pyre_test_python_testcase(gsl.pkg/vector_view.py)
# matrices
pyre_test_python_testcase(gsl.pkg/matrix_allocate.py)
pyre_test_python_testcase(gsl.pkg/matrix_zero.py)
pyre_test_python_testcase(gsl.pkg/matrix_fill.py)
pyre_test_python_testcase(gsl.pkg/matrix_random.py)
pyre_test_python_testcase(gsl.pkg/matrix_clone.py)
pyre_test_python_testcase(gsl.pkg/matrix_set.py)
pyre_test_python_testcase(gsl.pkg/matrix_slices.py)
pyre_test_python_testcase(gsl.pkg/matrix_contains.py)
pyre_test_python_testcase(gsl.pkg/matrix_tuple.py)
pyre_test_python_testcase(gsl.pkg/matrix_add.py)
pyre_test_python_testcase(gsl.pkg/matrix_sub.py)
pyre_test_python_testcase(gsl.pkg/matrix_mul.py)
pyre_test_python_testcase(gsl.pkg/matrix_div.py)
pyre_test_python_testcase(gsl.pkg/matrix_shift.py)
pyre_test_python_testcase(gsl.pkg/matrix_scale.py)
pyre_test_python_testcase(gsl.pkg/matrix_max.py)
pyre_test_python_testcase(gsl.pkg/matrix_min.py)
pyre_test_python_testcase(gsl.pkg/matrix_minmax.py)
pyre_test_python_testcase(gsl.pkg/matrix_view.py)
# blas
pyre_test_python_testcase(gsl.pkg/blas_ddot.py)
pyre_test_python_testcase(gsl.pkg/blas_dnrm2.py)
pyre_test_python_testcase(gsl.pkg/blas_dasum.py)
pyre_test_python_testcase(gsl.pkg/blas_daxpy.py)
pyre_test_python_testcase(gsl.pkg/blas_dgemv.py)
pyre_test_python_testcase(gsl.pkg/blas_dtrmv.py)
pyre_test_python_testcase(gsl.pkg/blas_dtrsv.py)
pyre_test_python_testcase(gsl.pkg/blas_dsymv.py)
pyre_test_python_testcase(gsl.pkg/blas_dgemm.py)
pyre_test_python_testcase(gsl.pkg/blas_dsymm.py)
pyre_test_python_testcase(gsl.pkg/blas_dtrmm.py)
# linalg
pyre_test_python_testcase(gsl.pkg/linalg_LU.py)
# stats
pyre_test_python_testcase(gsl.pkg/stats_correlation.py)
pyre_test_python_testcase(gsl.pkg/stats_covariance.py)

# if we have MPI
if(MPI_FOUND)
  # add osome more test cases
  pyre_test_python_testcase(gsl.pkg/matrix_bcast.py)
  pyre_test_python_testcase_mpi(gsl.pkg/matrix_bcast.py 8)
  pyre_test_python_testcase(gsl.pkg/matrix_collect.py)
  pyre_test_python_testcase_mpi(gsl.pkg/matrix_collect.py 8)
  pyre_test_python_testcase(gsl.pkg/matrix_partition.py)
  pyre_test_python_testcase_mpi(gsl.pkg/matrix_partition.py 8)
  pyre_test_python_testcase(gsl.pkg/vector_bcast.py)
  pyre_test_python_testcase_mpi(gsl.pkg/vector_bcast.py 8)
  pyre_test_python_testcase(gsl.pkg/vector_collect.py)
  pyre_test_python_testcase_mpi(gsl.pkg/vector_collect.py 8)
  pyre_test_python_testcase(gsl.pkg/vector_partition.py)
  pyre_test_python_testcase_mpi(gsl.pkg/vector_partition.py 8)
endif()


# end of file
