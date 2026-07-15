// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once


// my dependencies
#include "forward.h"


namespace pyre::tensor {

    // overload operator<< for vectors
    template <int D, typename T>
    std::ostream & operator<<(std::ostream & os, const vector_t<D, T> & vector);

    // overload operator<< for second order tensors
    template <int D1, int D2, typename T, class packingT>
    std::ostream & operator<<(std::ostream & os, const matrix_t<D1, D2, T, packingT> & tensor);

    // overload operator<< for quaternions
    template <typename T>
    std::ostream & operator<<(std::ostream & os, const UnitQuaternion<T> & quaternion);

    template <typename T>
    constexpr bool is_equal(T lhs, T rhs);

    template <typename T, class packingT, int... I>
    constexpr bool is_equal(
        const Tensor<T, packingT, I...> & lhs, const Tensor<T, packingT, I...> & rhs);

    template <typename T, class packingT, int... I>
    constexpr bool is_zero(const Tensor<T, packingT, I...> & A, T tolerance);

    template <typename T, class packingT, int... I>
    inline bool operator<(
        const Tensor<T, packingT, I...> & lhs, const Tensor<T, packingT, I...> & rhs);

} // namespace pyre::tensor


// get the inline definitions
#include "utilities.icc"


// end of file
