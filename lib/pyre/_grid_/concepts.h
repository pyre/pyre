// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// support
#include <concepts>


// add to the pyre::grid namespace
namespace pyre::grid::concepts {
    // the non-negative integers: the values that measure extents and label axes
    template <class T>
    concept InZ0 = std::unsigned_integral<T>;

    // a storage strategy is anything that knows how to name and reach its cells
    template <class S>
    concept StorageStrategy = requires {
        // it must publish the type of the cell it holds
        typename S::value_type;
        // along with the ways to point at a cell, mutably and not
        typename S::pointer;
        typename S::const_pointer;
        // and the ways to refer to a cell, mutably and not
        typename S::reference;
        typename S::const_reference;
    };

    // a packing strategy is anything that knows how to address a grid
    // for now we ask only that it name the type of its index; the rest of the
    // isomorphism from index space to memory offsets is not yet part of the contract
    template <class P>
    concept PackingStrategy = requires {
        // it must publish the type of the index it understands
        typename P::index_type;
    };

    // the guards that let a grid build its packing in place, from a tuple of arguments
    template <class P, class... PArgs>
    concept PackingConstructible = std::constructible_from<P, PArgs...>;

    // and the matching guard for building its storage in place
    template <class S, class... SArgs>
    concept StorageConstructible = std::constructible_from<S, SArgs...>;

} // namespace pyre::grid::concepts


// end of file
