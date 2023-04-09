// -*- c++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved


// code guard
#if !defined(pyre_algebra_externals_h)
#define pyre_algebra_externals_h


// externals
#include <cassert>
#include <cmath>
#include <functional>

// support
#include <pyre/journal.h>
#include <pyre/grid.h>
#include "machine_epsilon.h"

// aliases that define implementation choices
namespace pyre::algebra {

    // sequences of integers
    template <int N>
    using make_integer_sequence = std::make_integer_sequence<int, N>;
    template <int... I>
    using integer_sequence = std::integer_sequence<int, I...>;

}


#endif

// end of file
