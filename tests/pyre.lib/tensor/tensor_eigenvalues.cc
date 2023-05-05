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
int main(int argc, char* argv[]) {

    // 2D symmetric matrix
    constexpr symmetric_matrix_t<2> A { 1, 2, /*2,*/ 2 };

    // the matrix eigenvalues 
    constexpr auto lambda_A = eigenvalues(A); 
    constexpr auto eigenvalues_A = matrix_diagonal(lambda_A);

    // the matrix eigenvectors
    constexpr auto eigenvectors_A = eigenvectors(A);

    // 2D symmetric matrix: product of eigenvalues is equal to determinant
    static_assert(lambda_A[0] * lambda_A[1] == determinant(A));

    // 2D symmetric matrix: sum of eigenvalues is equal to trace
    static_assert(lambda_A[0] + lambda_A[1] == trace(A));

    // 2D symmetric matrix: definition of eigenvalues/vectors
    static_assert(A * col<0>(eigenvectors_A) == lambda_A[0] * col<0>(eigenvectors_A));
    static_assert(A * col<1>(eigenvectors_A) == lambda_A[1] * col<1>(eigenvectors_A));
    static_assert(A * eigenvectors_A == eigenvectors_A * eigenvalues_A);

    // 3D symmetric matrix
    constexpr symmetric_matrix_t<3> B { 1, -1, -2, 
                                         /*-1,*/  1,  1, 
                                         /*-2,*/ /*1,*/ 2 };

    // the matrix eigenvalues 
    constexpr auto lambda_B = eigenvalues(B); 
    constexpr auto eigenvalues_B = matrix_diagonal(lambda_B);

    // the matrix eigenvectors
    constexpr auto eigenvectors_B = eigenvectors(B);

    // 3D symmetric matrix: product of eigenvalues is equal to determinant
    static_assert(lambda_B[0] * lambda_B[1] * lambda_B[2] == determinant(B));

    // 3D symmetric matrix: sum of eigenvalues is equal to trace
    static_assert(lambda_B[0] + lambda_B[1] + lambda_B[2] == trace(B));

    // all done
    return 0;
}


// end of file
