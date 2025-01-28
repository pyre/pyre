// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// forward declarations
namespace pyre::typelists {
    // the basic data structure
    template <typename...>
    struct types_t;

    // prepend a type to the beginning of a type list
    template <typename...>
    struct prepend_t;

    // append a type to the end of a type list
    template <typename...>
    struct append_t;

    // merge typelists
    template <typename...>
    struct merge_t;

    // concatenate type lists
    template <typename...>
    struct concat_t;

    // the cartesian product of type lists
    template <typename...>
    struct cartesian_t;
} // namespace pyre::typelists


// end of file
