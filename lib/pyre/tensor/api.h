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
    // the zero tensor
    template <class tensorT>
    constexpr auto zero = make_zeros<tensorT>();

    // a tensor of ones
    template <class tensorT>
    constexpr auto ones = make_ones<tensorT>();

    // the identity tensor
    template <class tensorT>
    constexpr auto identity = make_identity<tensorT>();

    // the unit tensor with a one in the entry whose indices are specified in {J...}
    template <class tensorT, int... J>
    constexpr auto unit = make_basis_element<tensorT, J...>();

    // typedef for complex numbers
    using complex_t = std::complex<double>;

    // typedef for quaternions
    using quaternion_t = UnitQuaternion<complex_t>;

} // namespace pyre::tensor


// end of file
