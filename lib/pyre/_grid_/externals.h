// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include <array>
#include <cstddef>
#include <concepts>
#include <initializer_list>
#include <tuple>
#include <utility>

// support
#include <pyre/journal.h>
#include <pyre/memory.h>


// aliases that define implementation choices
namespace pyre::grid {
    // basic types
    using size_t = std::size_t;
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

    // sequences of integers
    template <int N>
    using make_integer_sequence = std::make_integer_sequence<int, N>;
    template <int... I>
    using integer_sequence = std::integer_sequence<int, I...>;

} // namespace pyre::grid


// end of file
