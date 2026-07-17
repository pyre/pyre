// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// forward declarations
namespace pyre::typelists {
    // the basic data structures
    template <typename...>
    struct types_t;

    template <template <typename...> class...>
    struct templates_t;

    // a value container, for iterating over non-type lists like (true, false) or (1, 2, 3, 4)
    template <auto...>
    struct values_t;

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

    // apply a list of templates to a list of types
    template <typename...>
    struct apply_t;

    // lift a value list into a type list of compile-time constants
    template <typename...>
    struct lift_t;

    // lower a type list of compile-time constants back into a value list
    template <typename...>
    struct lower_t;

} // namespace pyre::typelists


// end of file
