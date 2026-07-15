// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once


// my dependencies
#include "externals.h"


// set up the namespace
namespace pyre::tensor {

    // the tensor class
    template <typename T, class packingT, int... I>
    class Tensor;

    // alias for tensor
    template <typename T, class packingT, int... I>
    using tensor_t = Tensor<T, packingT, I...>;

    // the unit quaternion class
    template <typename T>
    class UnitQuaternion;

    // typedef for real values
    using real = double;
    // typedef for complex numbers
    using complex_t = std::complex<double>;

    // typedef for vectors
    template <int D, typename T = real, class packingT = pyre::grid::canonical_t<1, int>>
    using vector_t = Tensor<T, packingT, D>;
    // typedef for matrices
    template <int D1, int D2 = D1, typename T = real, class packingT = pyre::grid::canonical_t<2, int>>
    using matrix_t = Tensor<T, packingT, D1, D2>;
    // typedef for square matrices
    template <int D, typename T = real, class packingT = pyre::grid::canonical_t<2, int>>
    using square_matrix_t = matrix_t<D, D, T, packingT>;
    // typedef for symmetric matrices
    template <int D, typename T = real>
    using symmetric_matrix_t = matrix_t<D, D, T, pyre::grid::symmetric_t<2, int>>;
    // typedef for diagonal matrices
    template <int D, typename T = real>
    using diagonal_matrix_t = matrix_t<D, D, T, pyre::grid::diagonal_t<2, int>>;
    // typedef for fourth order tensors
    template <int D1, int D2 = D1, int D3 = D2, int D4 = D3, typename T = real>
    using fourth_order_tensor_t = Tensor<T, pyre::grid::canonical_t<4, int>, D1, D2, D3, D4>;
    // typedef for quaternions
    using quaternion_t = UnitQuaternion<complex_t>;

    // the zero tensor factory
    template <class tensorT>
    constexpr auto make_zeros() -> typename tensorT::diagonal_tensor_t;

    // the ones tensor factory
    template <class tensorT>
    constexpr auto make_ones() -> tensorT;

    // the identity tensor factory
    template <class tensorT>
    constexpr auto make_identity() -> typename tensorT::diagonal_tensor_t
        requires(tensorT::rank == 2);

    // returns whether the entries in a parameter pack {I...} are all equal
    template <int... I>
    constexpr auto entries_all_equal() -> bool;

    // the basis tensors factory (general version)
    template <class tensorT, int... I>
    constexpr auto make_basis_element() -> tensorT
        requires(
            sizeof...(I) == tensorT::rank &&
            // not a
            !(
                // diagonal entry
                entries_all_equal<I...>() &&
                // of a square tensor
                tensorT::is_square()));

    // the basis tensors factory (diagonal version)
    template <class tensorT, int... I>
    constexpr auto make_basis_element() -> typename tensorT::diagonal_tensor_t
        requires(
            sizeof...(I) == tensorT::rank &&
            // diagonal entry
            entries_all_equal<I...>() &&
            // of a square tensor
            tensorT::is_square());

} // namespace pyre::tensor


// end of file
