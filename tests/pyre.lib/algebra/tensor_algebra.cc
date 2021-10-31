// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// system includes
#include <iostream>
#include <cassert>

// dependencies
#include <pyre/algebra/Tensor.h>
#include <pyre/algebra/tensor_algebra.h>

using namespace pyre::algebra;

// main program
int main(int argc, char* argv[]) {

    // Matrix-vector product // TODO: { {0, 1, 2}, {3, 4, 5}, {6, 7, 8} }
    constexpr matrix_t<3, 3> A = { 1, -2, 0, 0, 1, 2, 0, 1, 1 };
    constexpr vector_t<3> x = { 1, 1, 1 };
    constexpr vector_t<3> y = A * x;
    static_assert(inv(A)*y == x);

    // product of eigenvalues is equal to determinant
    constexpr symmetric_matrix_t<2> C = { 1, 2, 2, 2 };
    constexpr auto lambda = eigenvalues(C); 
    static_assert(lambda[0] * lambda[1] == det(C));

    // definition of eigenvalues/vectors
    constexpr auto eigenvectorMatrix = eigenvectors(C);
    constexpr auto eigenvector0 = col<0>(eigenvectorMatrix);
    constexpr auto eigenvector1 = col<1>(eigenvectorMatrix);
    static_assert(C * eigenvector0 == lambda[0] * eigenvector0);
    static_assert(C * eigenvector1 == lambda[1] * eigenvector1);
    constexpr auto lambda_diag = matrix_diagonal(lambda);
    static_assert(C * eigenvectorMatrix ==  eigenvectorMatrix * lambda_diag);

    // Jacobi's theorem (all odd dimension skew symmetric matrices are singular)
    static_assert(det(skew(A)) == 0.0);

    constexpr matrix_t<2, 2> M = {0, 1, 2, 3};
    // symmetric tensors have zero skew part
    static_assert(skew(symmetric(M)) == matrix_t<2>::zero);



    constexpr matrix_t<2> unit00 = matrix_t<2>::unit(0, 0);
    constexpr matrix_t<2> unit01 = matrix_t<2>::unit(0, 1);
    constexpr matrix_t<2> unit10 = matrix_t<2>::unit(1, 0);
    constexpr matrix_t<2> unit11 = matrix_t<2>::unit(1, 1);

    constexpr vector_t<3> unit0 = vector_t<3>::unit(0);
    constexpr vector_t<3> unit1 = vector_t<3>::unit(1);
    constexpr vector_t<3> unit2 = vector_t<3>::unit(2);
    static_assert(unit0 + unit1 + unit2 == vector_t<3>::one);
    // QUESTION: How can this be constexpr if exp is not constexpr?
    constexpr auto my_exp = [](double x) { return exp(x); };
    constexpr auto C_exp = function(C, my_exp);
    static_assert(C_exp[{0, 1}] == C_exp[{1, 0}]);
    // static_assert(is_equal(function(function(C, my_exp), my_log), C));

    // all done
    return 0;
}


// end of file
