// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


#if !defined(pyre_tensor_algebra_h)
#define pyre_tensor_algebra_h


namespace pyre::tensor {

    // compute 2-norm of tensor
    template <typename T, class packingT, int... I>
    constexpr auto norm(const Tensor<T, packingT, I...> & tensor) -> T;

    // normalize a tensor with its 2-norm
    template <typename T, class packingT, int... I>
    constexpr auto normalize(const Tensor<T, packingT, I...> & tensor) -> Tensor<T, packingT, I...>;

    // tensors operator==
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator==(
        const Tensor<T, packingT1, I...> & lhs, const Tensor<T, packingT2, I...> & rhs) -> bool;

    // scalar times tensor
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(T2 a, const Tensor<T, packingT, I...> & y) -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>);

    // tensor times scalar
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(const Tensor<T, packingT, I...> & y, T2 a) -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>);

    // scalar times (temporary) tensor
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(T2 a, Tensor<T, packingT, I...> && y) -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>);

    // (temporary) tensor times scalar
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator*(Tensor<T, packingT, I...> && y, T2 a) -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>);

    // row-column vector product
    template <int D, typename T>
    constexpr auto operator*(const vector_t<D, T> & v1, const vector_t<D, T> & v2) -> T;

    // matrix-vector multiplication
    template <int D1, int D2, typename T, class packingT>
    constexpr auto operator*(const matrix_t<D1, D2, T, packingT> & A, const vector_t<D2, T> & v)
        -> vector_t<D1, T>;

    // vector-matrix multiplication
    template <int D1, int D2, typename T, class packingT>
    constexpr auto operator*(const vector_t<D2, T> & v, const matrix_t<D1, D2, T, packingT> & A)
        -> vector_t<D1, T>;

    // matrix-matrix multiplication
    template <int D1, int D2, int D3, typename T, class packingT1, class packingT2>
    constexpr auto operator*(
        const matrix_t<D1, D2, T, packingT1> & A1, const matrix_t<D2, D3, T, packingT2> & A2)
        -> matrix_t<D1, D3, T, typename repacking_prod<packingT1, packingT2>::packing_type>
        requires(D1 != 1 && D2 != 1 && D3 != 1);

    // tensor divided scalar
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator/(const Tensor<T, packingT, I...> & y, T2 a) -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>);

    // (temporary) tensor divided scalar
    template <typename T2, typename T, class packingT, int... I>
    constexpr auto operator/(Tensor<T, packingT, I...> && y, T2 a) -> Tensor<T, packingT, I...>
        requires(Tensor<T, packingT, I...>::size != 1 && std::convertible_to<T2, T>);

    // tensor plus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(
        const Tensor<T, packingT1, I...> & y1, const Tensor<T, packingT2, I...> & y2)
        -> Tensor<T, typename repacking_sum<packingT1, packingT2>::packing_type, I...>;

    // tensor plus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(
        const Tensor<T, packingT1, I...> & y1, Tensor<T, packingT2, I...> && y2)
        -> Tensor<T, packingT2, I...>
        requires(
            std::is_same_v<typename repacking_sum<packingT1, packingT2>::packing_type, packingT2>);

    // (temporary) tensor plus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(
        Tensor<T, packingT1, I...> && y1, const Tensor<T, packingT2, I...> & y2) -> auto;

    // (temporary) tensor plus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator+(Tensor<T, packingT1, I...> && y1, Tensor<T, packingT2, I...> && y2)
        -> auto;

    // (unary) minus tensor
    template <typename T, class packingT, int... I>
    constexpr auto operator-(const Tensor<T, packingT, I...> & y) -> Tensor<T, packingT, I...>;

    // (unary) minus (temporary) tensor
    template <typename T, class packingT, int... I>
    constexpr auto operator-(Tensor<T, packingT, I...> && y) -> auto;

    // tensor minus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(
        const Tensor<T, packingT1, I...> & y1, const Tensor<T, packingT2, I...> & y2) -> auto;

    // (temporary) tensor minus tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(
        Tensor<T, packingT1, I...> && y1, const Tensor<T, packingT2, I...> & y2) -> auto;

    // tensor minus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(
        const Tensor<T, packingT1, I...> & y1, Tensor<T, packingT2, I...> && y2) -> auto;

    // (temporary) tensor minus (temporary) tensor
    template <typename T, class packingT1, class packingT2, int... I>
    constexpr auto operator-(Tensor<T, packingT1, I...> && y1, Tensor<T, packingT2, I...> && y2)
        -> auto;

    // Tensor operator*=
    template <typename T, class packingT1, int... I, class TENSOR>
    constexpr auto operator*=(Tensor<T, packingT1, I...> & lhs, TENSOR && rhs)
        -> Tensor<T, packingT1, I...> &;

    // Tensor operator/=
    template <typename T, class packingT1, int... I, class SCALAR>
    constexpr auto operator/=(Tensor<T, packingT1, I...> & lhs, SCALAR && rhs)
        -> Tensor<T, packingT1, I...> &;

    // tensor plus equal tensor
    template <typename T, class packingT1, int... I, class TENSOR>
    constexpr auto operator+=(Tensor<T, packingT1, I...> & lhs, TENSOR && rhs)
        -> Tensor<T, packingT1, I...> &;

    // tensor minus equal tensor
    template <typename T, class packingT1, int... I, class TENSOR>
    constexpr auto operator-=(Tensor<T, packingT1, I...> & lhs, TENSOR && rhs)
        -> Tensor<T, packingT1, I...> &;

    // builds a square matrix with all zeros except the K-th row is equal to v
    template <int K, int D, typename T>
    constexpr auto matrix_row(const vector_t<D, T> & v) -> matrix_t<D, D, T>;

    // builds a square matrix with all zeros except the K-th column is equal to v
    template <int K, int D, typename T>
    constexpr auto matrix_column(const vector_t<D, T> & v) -> matrix_t<D, D, T>;

    // builds a square matrix with all zeros except the diagonal is equal to v
    template <int D, typename T>
    constexpr auto matrix_diagonal(const vector_t<D, T> & v) -> diagonal_matrix_t<D, T>;

    // builds the vector with the diagonal entries of a matrix
    template <int D, typename T, class packingT>
    constexpr auto matrix_diagonal(const matrix_t<D, D, T, packingT> & A) -> vector_t<D, T>;

    // the skew symmetric matrix representing vector a
    template <typename T>
    constexpr auto skew(const vector_t<3, T> & a) -> matrix_t<3, 3, T>;

    // the skew symmetric part of matrix A
    template <int D, typename T, class packingT>
    constexpr auto skew(const matrix_t<D, D, T, packingT> & A) -> auto
        requires(!std::is_same_v<packingT, pyre::grid::symmetric_t<2>>);

    // the skew symmetric part of a symmetric matrix (identically returns the zero tensor)
    template <int D, typename T>
    constexpr auto skew(const symmetric_matrix_t<D, T> & A) -> auto;

    // the symmetric part of a matrix
    template <int D, typename T, class packingT>
    constexpr auto symmetric(const matrix_t<D, D, T, packingT> & A) -> symmetric_matrix_t<D, T>;

    // the cross product between two 3D vectors
    template <typename T>
    constexpr auto cross(const vector_t<3, T> & a, const vector_t<3, T> & b) -> auto;

    // the cross product between two 2D vectors
    template <typename T>
    constexpr auto cross(const vector_t<2, T> & a, const vector_t<2, T> & b) -> T;

    // factorial
    template <int D>
    constexpr auto factorial() -> int;

    // the determinant of a 4x4 matrix
    template <typename T, class packingT>
    constexpr auto determinant(const matrix_t<4, 4, T, packingT> & A) -> T;

    // the determinant of a 3x3 matrix
    template <typename T, class packingT>
    constexpr auto determinant(const matrix_t<3, 3, T, packingT> & A) -> T;

    // the determinant of a 2x2 matrix
    template <typename T, class packingT>
    constexpr auto determinant(const matrix_t<2, 2, T, packingT> & A) -> T;

    // the inverse of a 3x3 matrix
    template <typename T, class packingT>
    constexpr auto inverse(const matrix_t<3, 3, T, packingT> & A) -> matrix_t<3, 3, T, packingT>;

    // the inverse of a 2x2 matrix
    template <typename T, class packingT>
    constexpr auto inverse(const matrix_t<2, 2, T, packingT> & A) -> matrix_t<2, 2, T, packingT>;

    // the trace of a matrix
    template <int D, typename T, class packingT>
    constexpr auto trace(const matrix_t<D, D, T, packingT> & A) -> T;

    // the transpose of a matrix
    template <int D1, int D2, typename T, class packingT>
    constexpr auto transpose(const matrix_t<D1, D2, T, packingT> & A)
        -> matrix_t<D2, D1, T, packingT>;

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
    template <int I, int D1, int D2, typename T, class packingT>
    constexpr auto row(const matrix_t<D1, D2, T, packingT> & A) -> vector_t<D2, T>;

    // extract column {I} of a matrix
    template <int I, int D1, int D2, typename T, class packingT>
    constexpr auto col(const matrix_t<D1, D2, T, packingT> & A) -> vector_t<D1, T>;

    // apply a function to a matrix
    // (this function does the spectral decomposition, applies the function to the diagonal
    // matrix of the eigenvalues and rebuilds the matrix)
    template <int D, typename T, class packingT>
    constexpr auto function(const matrix_t<D, D, T, packingT> & A, auto f) -> auto
        requires(
            std::is_same_v<packingT, pyre::grid::symmetric_t<2>>
            || std::is_same_v<packingT, pyre::grid::diagonal_t<2>>);

} // namespace pyre::tensor


// get the inline definitions
#define pyre_tensor_algebra_icc
#include "algebra.icc"
#undef pyre_tensor_algebra_icc


#endif

// end of file
