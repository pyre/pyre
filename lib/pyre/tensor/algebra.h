// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


#if !defined(pyre_tensor_algebra_h)
#define pyre_tensor_algebra_h


namespace pyre::tensor {

    // compute 2-norm of tensor
    template <tensor_c tensorT>
    constexpr auto norm(const tensorT & tensor) -> tensorT::scalar_type;

    // normalize a tensor with its 2-norm
    template <tensor_c tensorT>
    constexpr auto normalize(const tensorT & tensor) -> tensorT;

    // tensors operator==
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator==(const tensorT1 & lhs, const tensorT2 & rhs) -> bool;

    // scalar times tensor
    template <tensor_c tensorT>
    constexpr auto operator*(const typename tensorT::scalar_type & a, const tensorT & y) -> tensorT
        requires(tensorT::size != 1);

    // tensor times scalar
    template <tensor_c tensorT>
    constexpr auto operator*(const tensorT & y, const typename tensorT::scalar_type & a) -> tensorT
        requires(tensorT::size != 1);

    // scalar times (temporary) tensor
    template <tensor_c tensorT>
    constexpr auto operator*(const typename tensorT::scalar_type & a, tensorT && y) -> tensorT
        requires(tensorT::size != 1);

    // (temporary) tensor times scalar
    template <tensor_c tensorT>
    constexpr auto operator*(tensorT && y, const typename tensorT::scalar_type & a) -> tensorT
        requires(tensorT::size != 1);

    // row-column vector product
    template <vector_c vectorT1, vector_c vectorT2>
    constexpr auto operator*(const vectorT1 & v1, const vectorT2 & v2)
        -> product<vectorT1, vectorT2>::type
        requires(vectorT1::size == vectorT2::size);

    // matrix-vector multiplication (contract on matrix second index)
    template <matrix_c matrixT, vector_c vectorT>
    constexpr auto operator*(const matrixT & A, const vectorT & v)
        -> product<matrixT, vectorT>::type
        requires(matrixT::dims[1] == vectorT::size);

    // vector-matrix multiplication (contract on matrix first index)
    template <matrix_c matrixT, vector_c vectorT>
    constexpr auto operator*(const vectorT & v, const matrixT & A)
        -> product<vectorT, matrixT>::type
        requires(matrixT::dims[0] == vectorT::size);

    // matrix-matrix multiplication
    template <matrix_c matrixT1, matrix_c matrixT2>
    constexpr auto operator*(const matrixT1 & A1, const matrixT2 & A2)
        -> product<matrixT1, matrixT2>::type
        requires(matrixT1::dims[1] == matrixT2::dims[0]);

    // tensor divided scalar
    template <tensor_c tensorT>
    constexpr auto operator/(const tensorT & y, typename tensorT::scalar_type a) -> tensorT
        requires(tensorT::size != 1);

    // (temporary) tensor divided scalar
    template <tensor_c tensorT>
    constexpr auto operator/(tensorT && y, typename tensorT::scalar_type a) -> tensorT
        requires(tensorT::size != 1);

    // tensor plus tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator+(const tensorT1 & y1, const tensorT2 & y2) ->
        typename sum<tensorT1, tensorT2>::type
        requires(tensorT1::dims == tensorT2::dims);

    // tensor plus (temporary) tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator+(const tensorT1 & y1, tensorT2 && y2) -> tensorT2
        requires(
            tensorT1::dims == tensorT2::dims
            && std::is_same_v<typename sum<tensorT1, tensorT2>::type, tensorT2>);

    // (temporary) tensor plus tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator+(tensorT1 && y1, const tensorT2 & y2) -> tensorT1
        requires(
            tensorT1::dims == tensorT2::dims
            && std::is_same_v<typename sum<tensorT1, tensorT2>::type, tensorT1>);

    // (temporary) tensor plus (temporary) tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator+(tensorT1 && y1, tensorT2 && y2) -> tensorT1
        requires(
            tensorT1::dims == tensorT2::dims
            && std::is_same_v<typename sum<tensorT1, tensorT2>::type, tensorT1>);

    // (temporary) tensor plus (temporary) tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator+(tensorT1 && y1, tensorT2 && y2) -> tensorT2
        requires(
            tensorT1::dims == tensorT2::dims
            && std::is_same_v<typename sum<tensorT1, tensorT2>::type, tensorT2>
            && !std::is_same_v<typename sum<tensorT1, tensorT2>::type, tensorT1>);

    // (unary) minus tensor
    template <tensor_c tensorT>
    constexpr auto operator-(const tensorT & y) -> tensorT;

    // (unary) minus (temporary) tensor
    template <tensor_c tensorT>
    constexpr auto operator-(tensorT && y) -> tensorT;

    // tensor minus tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator-(const tensorT1 & y1, const tensorT2 & y2) -> auto
        requires(tensorT1::dims == tensorT2::dims);

    // (temporary) tensor minus tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator-(tensorT1 && y1, const tensorT2 & y2) -> auto
        requires(tensorT1::dims == tensorT2::dims);

    // tensor minus (temporary) tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator-(const tensorT1 & y1, tensorT2 && y2) -> auto
        requires(tensorT1::dims == tensorT2::dims);


    // (temporary) tensor minus (temporary) tensor
    template <tensor_c tensorT1, tensor_c tensorT2>
    constexpr auto operator-(tensorT1 && y1, tensorT2 && y2) -> auto
        requires(tensorT1::dims == tensorT2::dims);

    // Tensor operator*=
    template <tensor_c tensorT, class TENSOR>
    constexpr auto operator*=(tensorT & lhs, TENSOR && rhs) -> tensorT &;

    // Tensor operator/=
    template <tensor_c tensorT, class SCALAR>
    constexpr auto operator/=(tensorT & lhs, SCALAR && rhs) -> tensorT &;

    // tensor plus equal tensor
    template <tensor_c tensorT, class TENSOR>
    constexpr auto operator+=(tensorT & lhs, TENSOR && rhs) -> tensorT &;

    // tensor minus equal tensor
    template <tensor_c tensorT, class TENSOR>
    constexpr auto operator-=(tensorT & lhs, TENSOR && rhs) -> tensorT &;

    // builds a square matrix with all zeros except the K-th row is equal to v
    template <int K, class packingT = pyre::grid::canonical_t<2>, vector_c vectorT>
    constexpr auto matrix_row(const vectorT & v)
        -> matrix_t<vectorT::size, vectorT::size, typename vectorT::scalar_type, packingT>;

    // builds a square matrix with all zeros except the K-th column is equal to v
    template <int K, class packingT = pyre::grid::canonical_t<2>, vector_c vectorT>
    constexpr auto matrix_column(const vectorT & v)
        -> matrix_t<vectorT::size, vectorT::size, typename vectorT::scalar_type, packingT>;

    // builds a square matrix with all zeros except the diagonal is equal to v
    template <vector_c vectorT>
    constexpr auto matrix_diagonal(const vectorT & v)
        -> diagonal_matrix_t<vectorT::size, typename vectorT::scalar_type>;

    // builds the vector with the diagonal entries of a matrix
    template <square_matrix_c matrixT>
    constexpr auto matrix_diagonal(const matrixT & A)
        -> vector_t<matrixT::dims[0], typename matrixT::scalar_type>;

    // the skew symmetric matrix representing vector {a}
    template <vector_c vectorT, class packingT = pyre::grid::canonical_t<2>>
    constexpr auto skew(const vectorT & a)
        -> square_matrix_t<3, typename vectorT::scalar_type, packingT>
        requires(vectorT::size == 3);

    // the skew symmetric part of a square matrix
    template <square_matrix_c matrixT>
    constexpr auto skew(const matrixT & A) -> auto;

    // the symmetric part of a square matrix
    template <square_matrix_c matrixT>
    constexpr auto symmetric(const matrixT & A) -> typename matrixT::symmetric_tensor_t;

    // the cross product between two 3D vectors
    template <vector_c vectorT>
    constexpr auto cross(const vectorT & a, const vectorT & b) -> auto
        requires(vectorT::size == 3);

    // the cross product between two 2D vectors
    template <vector_c vectorT>
    constexpr auto cross(const vectorT & a, const vectorT & b) -> typename vectorT::scalar_type;

    // factorial
    template <int D>
    constexpr auto factorial() -> int;

    // the determinant of a 4x4 matrix
    template <typename T, class packingT>
    constexpr auto determinant(const square_matrix_t<4, T, packingT> & A) -> T;

    // the determinant of a 3x3 matrix
    template <typename T, class packingT>
    constexpr auto determinant(const square_matrix_t<3, T, packingT> & A) -> T;

    // the determinant of a 2x2 matrix
    template <typename T, class packingT>
    constexpr auto determinant(const square_matrix_t<2, T, packingT> & A) -> T;

    // the determinant of a 1x1 matrix
    template <typename T, class packingT>
    constexpr auto determinant(const square_matrix_t<1, T, packingT> & A) -> T;

    // the inverse of a 3x3 matrix
    template <typename T, class packingT>
    constexpr auto inverse(const square_matrix_t<3, T, packingT> & A)
        -> square_matrix_t<3, T, packingT>;

    // the inverse of a 2x2 matrix
    template <typename T, class packingT>
    constexpr auto inverse(const square_matrix_t<2, T, packingT> & A)
        -> square_matrix_t<2, T, packingT>;

    // the inverse of a 1x1 matrix
    template <typename T, class packingT>
    constexpr auto inverse(const square_matrix_t<1, T, packingT> & A)
        -> square_matrix_t<1, T, packingT>;

    // the trace of a matrix
    template <square_matrix_c matrixT>
    constexpr auto trace(const matrixT & A) -> typename matrixT::scalar_type;

    // the transpose of a matrix
    template <int D1, int D2, typename T, class packingT>
    constexpr auto transpose(const matrix_t<D1, D2, T, packingT> & A)
        -> matrix_t<D2, D1, T, packingT>;

    // the transpose of a vector
    template <int D, typename T>
    constexpr auto transpose(const vector_t<D, T> & v) -> vector_t<D, T>;

    // the eigenvalues of a 2x2 matrix
    template <typename T>
    constexpr auto eigenvalues(const symmetric_matrix_t<2, T> & A) -> vector_t<2, T>;

    // the eigenvectors of a 2x2 matrix
    template <typename T>
    constexpr auto eigenvectors(const symmetric_matrix_t<2, T> & A) -> matrix_t<2, 2, T>;

    // the eigenvalues of a 3x3 matrix
    template <typename T>
    constexpr auto eigenvalues(const symmetric_matrix_t<3, T> & A) -> vector_t<3, T>;

    // the eigenvectors of a 3x3 matrix
    template <typename T>
    constexpr auto eigenvectors(const symmetric_matrix_t<3, T> & A) -> matrix_t<3, 3, T>;

    // the eigenvalues of a diagonal matrix
    template <int D, typename T>
    constexpr auto eigenvalues(const diagonal_matrix_t<D, T> & A) -> auto;

    // the eigenvectors of a diagonal matrix
    template <int D, typename T>
    constexpr auto eigenvectors(const diagonal_matrix_t<D, T> & A) -> auto;

    // extract row {I} of a matrix
    template <int I, matrix_c matrixT>
    constexpr auto row(const matrixT & A)
        -> vector_t<matrixT::dims[1], typename matrixT::scalar_type>;

    // extract column {I} of a matrix
    template <int I, matrix_c matrixT>
    constexpr auto col(const matrixT & A)
        -> vector_t<matrixT::dims[0], typename matrixT::scalar_type>;

    // apply a function to a matrix
    // (this function does the spectral decomposition, applies the function to the diagonal
    // matrix of the eigenvalues and rebuilds the matrix)
    template <square_matrix_c matrixT>
    constexpr auto function(const matrixT & A, auto f) -> auto
        requires(
            std::is_same_v<typename matrixT::pack_t, pyre::grid::symmetric_t<2>>
            || std::is_same_v<typename matrixT::pack_t, pyre::grid::diagonal_t<2>>);

} // namespace pyre::tensor


// get the inline definitions
#define pyre_tensor_algebra_icc
#include "algebra.icc"
#undef pyre_tensor_algebra_icc


#endif

// end of file
