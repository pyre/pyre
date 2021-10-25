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

// main program
int main(int argc, char* argv[]) {

    pyre::algebra::vector_t<2> vector1 = { 0.0, 0.0 };
    assert(vector1 == vector1);

    constexpr pyre::algebra::vector_t<2> vector2 = { 1.0, 2.0 };
    vector1 += vector2;
    assert(vector1 + vector2 == 2.0 * vector2);
    static_assert(vector2 + vector2 == 2.0 * vector2);
    static_assert(vector2 - vector2 == pyre::algebra::vector_t<2>::zero);
    static_assert(pyre::algebra::vector_t<2>::zero
        == pyre::algebra::vector_t<2>::one - pyre::algebra::vector_t<2>::one);

    constexpr pyre::algebra::scalar_t a = 1.0;
    static_assert(vector2 * a == vector2);
    static_assert(vector2 * (-a) == -vector2);
    static_assert((-a) * vector2 == -vector2);
    static_assert(vector2 / a == vector2);
    static_assert(vector2 / (-a) == -vector2);

    constexpr pyre::algebra::vector_t<3> vector3 = { 1, 0, 0 };
    constexpr pyre::algebra::vector_t<3> vector4 = { 0, 1, 0 };
    static_assert(transpose(vector3) * vector4 == 0.0);

    constexpr pyre::algebra::scalar_t b(1.0);
    static_assert(2 * b == b + 1);

    // TODO: Add tests for all algebraic operators

    // Matrix-vector product // TODO: { {0, 1, 2}, {3, 4, 5}, {6, 7, 8} }
    constexpr pyre::algebra::matrix_t<3, 3> A = { 1, -2, 0, 0, 1, 2, 0, 1, 1 };
    constexpr pyre::algebra::vector_t<3> x = { 1, 1, 1 };
    constexpr pyre::algebra::vector_t<3> y = a * A * x;
    static_assert(inv(A)*y == a * x);

    // transpose tensor
    constexpr pyre::algebra::matrix_t<3, 3> B = transpose(A);
    // transpose of transpose is the identity operator
    static_assert(transpose(B) == A);

    // transpose preserves trace
    constexpr pyre::algebra::scalar_t traceA = tr(A);
    constexpr pyre::algebra::scalar_t traceB = tr(B);
    static_assert(traceA == traceB);

    // transpose preserves determinant
    constexpr pyre::algebra::scalar_t detA = det(A);
    constexpr pyre::algebra::scalar_t detB = det(B);
    static_assert(det(B) == det(A));

    // product of eigenvalues is equal to determinant
    constexpr pyre::algebra::symmetric_matrix_t<2> C = { 1, 2, 2, 2 };
    constexpr auto lambda = eigenvalues(C); 
    static_assert(lambda[0] * lambda[1] == det(C));

    // definition of eigenvalues/vectors
    constexpr auto eigenvectorMatrix = eigenvectors(C);
    constexpr auto eigenvector0 = col<0>(eigenvectorMatrix);
    constexpr auto eigenvector1 = col<1>(eigenvectorMatrix);
    static_assert(C * eigenvector0 == lambda[0] * eigenvector0);
    static_assert(C * eigenvector1 == lambda[1] * eigenvector1);

    // Jacobi's theorem (all odd dimension skew symmetric matrices are singular)
    static_assert(det(skew(A)) == 0.0);

    constexpr pyre::algebra::matrix_t<2, 2> M = {0, 1, 2, 3};
    // symmetric tensors have zero skew part
    static_assert(skew(sym(M)) == pyre::algebra::matrix_t<2>::zero);
    // Cayley-Hamilton's theorem (a matrix is a solution of its characteristic polynomial) (2D)
    constexpr pyre::algebra::matrix_t<2, 2> I = { 1, 0, 0, 1 };
    static_assert(M * M - tr(M) * M + det(M) * I == pyre::algebra::matrix_t<2>::zero);

    static_assert(pyre::algebra::matrix_t<2>::zero == pyre::algebra::matrix_t<2>::zero);
    static_assert(M == M);

    constexpr pyre::algebra::matrix_t<2> unit00 = pyre::algebra::matrix_t<2>::unit<{0, 0}>;
    constexpr pyre::algebra::matrix_t<2> unit01 = pyre::algebra::matrix_t<2>::unit<{0, 1}>;
    constexpr pyre::algebra::matrix_t<2> unit10 = pyre::algebra::matrix_t<2>::unit<{1, 0}>;
    constexpr pyre::algebra::matrix_t<2> unit11 = pyre::algebra::matrix_t<2>::unit<{1, 1}>;
    static_assert(unit00 == pyre::algebra::matrix_t<2>{1, 0, 0, 0});
    static_assert(unit01 == pyre::algebra::matrix_t<2>{0, 1, 0, 0});
    static_assert(unit10 == pyre::algebra::matrix_t<2>{0, 0, 1, 0});
    static_assert(unit11 == pyre::algebra::matrix_t<2>{0, 0, 0, 1});
    static_assert(unit00 + unit01 + unit10 + unit11 == pyre::algebra::matrix_t<2>::one);

    constexpr pyre::algebra::vector_t<3> unit0 = pyre::algebra::vector_t<3>::unit<{0, 0}>;
    constexpr pyre::algebra::vector_t<3> unit1 = pyre::algebra::vector_t<3>::unit<{1, 0}>;
    constexpr pyre::algebra::vector_t<3> unit2 = pyre::algebra::vector_t<3>::unit<{2, 0}>;
    static_assert(unit0 == pyre::algebra::vector_t<3>{1, 0, 0});
    static_assert(unit1 == pyre::algebra::vector_t<3>{0, 1, 0});
    static_assert(unit2 == pyre::algebra::vector_t<3>{0, 0, 1});

    // all done
    return 0;
}


// end of file
