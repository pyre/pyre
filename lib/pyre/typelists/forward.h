// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// forward declarations
namespace pyre::typelists {
    // a declarator of a given type {T}; the dummy {int} argument is used while expanding parameter
    // packs
    template <typename T, int>
    struct type_t;

    // a collection of types
    template <typename...>
    struct types_t;

    // a collection of {N} copies of the type {T}
    template <typename T, int N, typename seqT = std::make_index_sequence<N>>
    struct list_t;

    // turning type lists into tuples
    template <typename...>
    struct tuple_t;

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

    // a collection of templates
    template <template <typename...> class...>
    struct templates_t;
} // namespace pyre::typelists


// end of file
