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

    constexpr vector_t<3> vector3 = { 1, 0, 0 };
    constexpr vector_t<3> vector4 = { 0, 1, 0 };
    static_assert(vector3 * vector4 == 0.0);

    // Matrix-vector product // TODO: { {0, 1, 2}, {3, 4, 5}, {6, 7, 8} }
    constexpr matrix_t<3, 3> A = { 1, -2, 0, 0, 1, 2, 0, 1, 1 };
    constexpr vector_t<3> x = { 1, 1, 1 };
    constexpr vector_t<3> y = a * A * x;
    static_assert(inv(A)*y == a * x);

    // transpose tensor
    constexpr matrix_t<3, 3> B = transpose(A);
    // transpose of transpose is the identity operator
    static_assert(transpose(B) == A);

    // transpose preserves trace
    constexpr scalar_t traceA = tr(A);
    constexpr scalar_t traceB = tr(B);
    static_assert(traceA == traceB);

    // transpose preserves determinant
    constexpr scalar_t detA = det(A);
    constexpr scalar_t detB = det(B);
    static_assert(det(B) == det(A));

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
    // Cayley-Hamilton's theorem (a matrix is a solution of its characteristic polynomial) (2D)
    static_assert(M * M - tr(M) * M + det(M) * identity_matrix<2> == zero_matrix<2>);

    static_assert(zero_matrix<2> == matrix_t<2>::zero);
    static_assert(M == M);

    static_assert(unit<2>(0) == vector_t<2>{1, 0}); 
    static_assert(unit<2>(1) == vector_t<2>{0, 1}); 

    static_assert(unit<3>(0) == vector_t<3>{1, 0, 0}); 
    static_assert(unit<3>(1) == vector_t<3>{0, 1, 0}); 
    static_assert(unit<3>(2) == vector_t<3>{0, 0, 1}); 

    static_assert(unit<2>(0, 0) == matrix_t<2>{1, 0, 0, 0}); 
    static_assert(unit<2>(0, 1) == matrix_t<2>{0, 1, 0, 0}); 
    static_assert(unit<2>(1, 0) == matrix_t<2>{0, 0, 1, 0}); 
    static_assert(unit<2>(1, 1) == matrix_t<2>{0, 0, 0, 1}); 

    static_assert(unit<3>(0, 0) == matrix_t<3>{1, 0, 0, 0, 0, 0, 0, 0, 0}); 
    static_assert(unit<3>(0, 1) == matrix_t<3>{0, 1, 0, 0, 0, 0, 0, 0, 0}); 
    static_assert(unit<3>(0, 2) == matrix_t<3>{0, 0, 1, 0, 0, 0, 0, 0, 0}); 
    static_assert(unit<3>(1, 0) == matrix_t<3>{0, 0, 0, 1, 0, 0, 0, 0, 0}); 
    static_assert(unit<3>(1, 1) == matrix_t<3>{0, 0, 0, 0, 1, 0, 0, 0, 0}); 
    static_assert(unit<3>(1, 2) == matrix_t<3>{0, 0, 0, 0, 0, 1, 0, 0, 0}); 
    static_assert(unit<3>(2, 0) == matrix_t<3>{0, 0, 0, 0, 0, 0, 1, 0, 0}); 
    static_assert(unit<3>(2, 1) == matrix_t<3>{0, 0, 0, 0, 0, 0, 0, 1, 0}); 
    static_assert(unit<3>(2, 2) == matrix_t<3>{0, 0, 0, 0, 0, 0, 0, 0, 1}); 

    constexpr matrix_t<2> unit00 = matrix_t<2>::unit(0, 0);
    constexpr matrix_t<2> unit01 = matrix_t<2>::unit(0, 1);
    constexpr matrix_t<2> unit10 = matrix_t<2>::unit(1, 0);
    constexpr matrix_t<2> unit11 = matrix_t<2>::unit(1, 1);
    static_assert(unit00 == matrix_t<2>{1, 0, 0, 0});
    static_assert(unit01 == matrix_t<2>{0, 1, 0, 0});
    static_assert(unit10 == matrix_t<2>{0, 0, 1, 0});
    static_assert(unit11 == matrix_t<2>{0, 0, 0, 1});
    static_assert(unit00 + unit01 + unit10 + unit11 == matrix_t<2>::one);

    constexpr vector_t<3> unit0 = vector_t<3>::unit(0);
    constexpr vector_t<3> unit1 = vector_t<3>::unit(1);
    constexpr vector_t<3> unit2 = vector_t<3>::unit(2);
    static_assert(unit0 == vector_t<3>{1, 0, 0});
    static_assert(unit1 == vector_t<3>{0, 1, 0});
    static_assert(unit2 == vector_t<3>{0, 0, 1});
    static_assert(unit0 + unit1 + unit2 == vector_t<3>::one);
    // QUESTION: How can this be constexpr if exp is not constexpr?
    constexpr auto my_exp = [](double x) { return exp(x); };
    constexpr auto C_exp = function(C, my_exp);
    static_assert(C_exp[{0, 1}] == C_exp[{1, 0}]);
    // static_assert(is_equal(function(function(C, my_exp), my_log), C));

    static_assert(matrix_diagonal(identity_matrix<3>) == vector_t<3>::one);
    static_assert(matrix_diagonal(matrix_diagonal(identity_matrix<3>)) == identity_matrix<3>);

    // all done
    return 0;
}


// end of file
