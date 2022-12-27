// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_externals_h)
#define pyre_grid_externals_h


// externals
#include <array>
#include <algorithm>
#include <iterator>
#include <numeric>
#include <ostream>

// support
#include <pyre/journal.h>
#include <pyre/memory.h>


// aliases that define implementation choices
namespace pyre::grid {
    // make sure we are on the same page as {memory} on these fundamental types
    // strings
    using string_t = pyre::memory::string_t;
    // names of things
    using name_t = pyre::memory::name_t;
    // filenames
    using uri_t = pyre::memory::uri_t;

    // arrays of things
    template <typename T, int N>
    using array_t = std::array<T, N>;

    // for the result of scaling reps by doubles
    template <int N>
    using doubles_t = std::array<double, N>;

    // for the result of scaling reps by floats
    template <int N>
    using floats_t = std::array<float, N>;

    // output streams
    using ostream_t = std::ostream;
    using ostream_reference = std::ostream &;
} // namespace pyre::grid


#endif

// end of file
