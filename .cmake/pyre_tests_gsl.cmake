# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# gsl
#
# sanity
pyre_test_python_testcase(gsl/sanity.py)
# general
pyre_test_python_testcase(gsl/rng.py)
pyre_test_python_testcase(gsl/pdf.py)
pyre_test_python_testcase(gsl/permutation.py)
pyre_test_python_testcase(gsl/vector.py)
pyre_test_python_testcase(gsl/matrix.py)
pyre_test_python_testcase(gsl/blas.py)
pyre_test_python_testcase(gsl/linalg.py)
# random numbers
pyre_test_python_testcase(gsl/rng_available.py)
pyre_test_python_testcase(gsl/rng_allocate.py)
pyre_test_python_testcase(gsl/rng_range.py)
pyre_test_python_testcase(gsl/rng_int.py)
pyre_test_python_testcase(gsl/rng_float.py)
# pdfs
pyre_test_python_testcase(gsl/pdf_uniform.py)
pyre_test_python_testcase(gsl/pdf_uniform_pos.py)
pyre_test_python_testcase(gsl/pdf_gaussian.py)
pyre_test_python_testcase(gsl/pdf_dirichlet.py)
# permutations
pyre_test_python_testcase(gsl/permutation_allocate.py)
pyre_test_python_testcase(gsl/permutation_copy.py)
pyre_test_python_testcase(gsl/permutation_get.py)
# vectors
pyre_test_python_testcase(gsl/vector_allocate.py)
pyre_test_python_testcase(gsl/vector_zero.py)
pyre_test_python_testcase(gsl/vector_fill.py)
pyre_test_python_testcase(gsl/vector_random.py)
pyre_test_python_testcase(gsl/vector_clone.py)
pyre_test_python_testcase(gsl/vector_set.py)
pyre_test_python_testcase(gsl/vector_slices.py)
pyre_test_python_testcase(gsl/vector_contains.py)
pyre_test_python_testcase(gsl/vector_tuple.py)
pyre_test_python_testcase(gsl/vector_add.py)
pyre_test_python_testcase(gsl/vector_sub.py)
pyre_test_python_testcase(gsl/vector_mul.py)
pyre_test_python_testcase(gsl/vector_div.py)
pyre_test_python_testcase(gsl/vector_shift.py)
pyre_test_python_testcase(gsl/vector_scale.py)
pyre_test_python_testcase(gsl/vector_max.py)
pyre_test_python_testcase(gsl/vector_min.py)
pyre_test_python_testcase(gsl/vector_minmax.py)
pyre_test_python_testcase(gsl/vector_view.py)
# matrices
pyre_test_python_testcase(gsl/matrix_allocate.py)
pyre_test_python_testcase(gsl/matrix_zero.py)
pyre_test_python_testcase(gsl/matrix_fill.py)
pyre_test_python_testcase(gsl/matrix_random.py)
pyre_test_python_testcase(gsl/matrix_clone.py)
pyre_test_python_testcase(gsl/matrix_set.py)
pyre_test_python_testcase(gsl/matrix_slices.py)
pyre_test_python_testcase(gsl/matrix_contains.py)
pyre_test_python_testcase(gsl/matrix_tuple.py)
pyre_test_python_testcase(gsl/matrix_add.py)
pyre_test_python_testcase(gsl/matrix_sub.py)
pyre_test_python_testcase(gsl/matrix_mul.py)
pyre_test_python_testcase(gsl/matrix_div.py)
pyre_test_python_testcase(gsl/matrix_shift.py)
pyre_test_python_testcase(gsl/matrix_scale.py)
pyre_test_python_testcase(gsl/matrix_max.py)
pyre_test_python_testcase(gsl/matrix_min.py)
pyre_test_python_testcase(gsl/matrix_minmax.py)
pyre_test_python_testcase(gsl/matrix_view.py)
# blas
pyre_test_python_testcase(gsl/blas_ddot.py)
pyre_test_python_testcase(gsl/blas_dnrm2.py)
pyre_test_python_testcase(gsl/blas_dasum.py)
pyre_test_python_testcase(gsl/blas_daxpy.py)
pyre_test_python_testcase(gsl/blas_dgemv.py)
pyre_test_python_testcase(gsl/blas_dtrmv.py)
pyre_test_python_testcase(gsl/blas_dtrsv.py)
pyre_test_python_testcase(gsl/blas_dsymv.py)
pyre_test_python_testcase(gsl/blas_dgemm.py)
pyre_test_python_testcase(gsl/blas_dsymm.py)
pyre_test_python_testcase(gsl/blas_dtrmm.py)
# linalg
pyre_test_python_testcase(gsl/linalg_LU.py)
# stats
pyre_test_python_testcase(gsl/stats_correlation.py)
pyre_test_python_testcase(gsl/stats_covariance.py)

# if we have MPI
if(MPI_FOUND)
  # add osome more test cases
  pyre_test_python_testcase(gsl/matrix_bcast.py)
  pyre_test_python_testcase_mpi(gsl/matrix_bcast.py 8)
  pyre_test_python_testcase(gsl/matrix_collect.py)
  pyre_test_python_testcase_mpi(gsl/matrix_collect.py 8)
  pyre_test_python_testcase(gsl/matrix_partition.py)
  pyre_test_python_testcase_mpi(gsl/matrix_partition.py 8)
  pyre_test_python_testcase(gsl/vector_bcast.py)
  pyre_test_python_testcase_mpi(gsl/vector_bcast.py 8)
  pyre_test_python_testcase(gsl/vector_collect.py)
  pyre_test_python_testcase_mpi(gsl/vector_collect.py 8)
  pyre_test_python_testcase(gsl/vector_partition.py)
  pyre_test_python_testcase_mpi(gsl/vector_partition.py 8)
endif()


# end of file
