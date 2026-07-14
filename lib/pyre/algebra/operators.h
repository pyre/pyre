// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


namespace pyre::algebra {

    // binary operators
    template <typename numeric_t>
    inline numeric_t operator+(const numeric_t &, const numeric_t &);

    template <typename numeric_t>
    inline numeric_t operator-(const numeric_t &, const numeric_t &);

    template <typename numeric_t>
    inline numeric_t operator*(const numeric_t &, const numeric_t &);

    template <typename numeric_t>
    inline numeric_t operator/(const numeric_t &, const numeric_t &);
} // namespace pyre::algebra

// get the inline definitions
#include "operators.icc"


// end of file
