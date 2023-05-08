// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/tensor.h>


// use namespace for readability
using namespace pyre::tensor;


// main program
int
main(int argc, char * argv[])
{
    {
        // the packing-agnostic canonical basis of R^2x2
        constexpr auto e_00 = matrix_t<2>::unit<0, 0>;
        constexpr auto e_01 = matrix_t<2>::unit<0, 1>;
        constexpr auto e_10 = matrix_t<2>::unit<1, 0>;
        constexpr auto e_11 = matrix_t<2>::unit<1, 1>;
        constexpr auto e_01s = symmetric(e_01 + e_10);

        // a symmetric matrix in R^2x2
        constexpr auto A = 1.0 * e_00 + 2.0 * e_01s + 2.0 * e_11;

        // the matrix eigenvalues
        constexpr auto lambda_A = eigenvalues(A);
        constexpr auto eigenvalues_A = matrix_diagonal(lambda_A);

        // the matrix eigenvectors
        constexpr auto eigenvectors_A = eigenvectors(A);

        // product of eigenvalues is equal to determinant
        static_assert(lambda_A[0] * lambda_A[1] == determinant(A));

        // sum of eigenvalues is equal to trace
        static_assert(lambda_A[0] + lambda_A[1] == trace(A));

        // definition of eigenvalues/vectors pair
        static_assert(A * col<0>(eigenvectors_A) == lambda_A[0] * col<0>(eigenvectors_A));
        static_assert(A * col<1>(eigenvectors_A) == lambda_A[1] * col<1>(eigenvectors_A));

        // spectral decomposition
        static_assert(A * eigenvectors_A == eigenvectors_A * eigenvalues_A);
    }


    {
        // the packing-agnostic canonical basis of R^3x3
        constexpr auto e_00 = matrix_t<3>::unit<0, 0>;
        constexpr auto e_01 = matrix_t<3>::unit<0, 1>;
        constexpr auto e_02 = matrix_t<3>::unit<0, 2>;
        constexpr auto e_10 = matrix_t<3>::unit<1, 0>;
        constexpr auto e_11 = matrix_t<3>::unit<1, 1>;
        constexpr auto e_12 = matrix_t<3>::unit<1, 2>;
        constexpr auto e_20 = matrix_t<3>::unit<2, 0>;
        constexpr auto e_21 = matrix_t<3>::unit<2, 1>;
        constexpr auto e_22 = matrix_t<3>::unit<2, 2>;
        constexpr auto e_01s = symmetric(e_01 + e_10);
        constexpr auto e_02s = symmetric(e_02 + e_20);
        constexpr auto e_12s = symmetric(e_12 + e_21);

        // a symmetric matrix in R^3x3
        constexpr auto B =
            1.0 * e_00 - 1.0 * e_01s - 2.0 * e_02s + 1.0 * e_11 + 1.0 * e_12s + 2.0 * e_22;

        // the matrix eigenvalues
        constexpr auto lambda_B = eigenvalues(B);
        constexpr auto eigenvalues_B = matrix_diagonal(lambda_B);

        // the matrix eigenvectors
        constexpr auto eigenvectors_B = eigenvectors(B);

        // product of eigenvalues is equal to determinant
        static_assert(lambda_B[0] * lambda_B[1] * lambda_B[2] == determinant(B));

        // sum of eigenvalues is equal to trace
        static_assert(lambda_B[0] + lambda_B[1] + lambda_B[2] == trace(B));
    }


    // all done
    return 0;
}


// end of file
