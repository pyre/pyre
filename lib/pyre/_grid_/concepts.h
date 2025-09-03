// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// support
#include <concepts>


// add to the pyre::grid namespace
namespace pyre::grid::concepts {
    // members of Z0
    template <class T>
    concept InZ0 = std::unsigned_integral<T>;

    // requirements for storage strategies
    template <class S>
    concept StorageStrategy = requires {
        // for the storage cell
        typename S::value_type;
        typename S::pointer;
        typename S::const_pointer;
        typename S::reference;
        typename S::const_reference;
    };

    // requirements for packing strategies
    template <class P>
    concept PackingStrategy = requires {
        // an index
        typename P::index_type;
    };

    // piecewise construction
    template <class P, class... PArgs>
    concept PackingConstructible = std::constructible_from<P, PArgs...>;

    template <class S, class... SArgs>
    concept StorageConstructible = std::constructible_from<S, SArgs...>;

} // namespace pyre::grid::concepts


// end of file
