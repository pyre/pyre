// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved


// code guard
#if !defined(pyre_tensor_externals_h)
#define pyre_tensor_externals_h


// externals
#include <cassert>
#include <cmath>
#include <functional>

// support
#include <pyre/journal.h>
#include <pyre/grid.h>
#include <pyre/algebra/epsilon.h>


// aliases that define implementation choices
namespace pyre::tensor {

    // sequences of integers
    template <int N>
    using make_integer_sequence = std::make_integer_sequence<int, N>;
    template <int... I>
    using integer_sequence = std::integer_sequence<int, I...>;

} // namespace pyre::tensor


#endif

// end of file
