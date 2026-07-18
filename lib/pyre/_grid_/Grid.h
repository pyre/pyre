// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// a multi-dimensional array: a packing strategy {P} that says how index space maps to
// memory offsets, married to a storage strategy {S} that owns the cells
// currently this is just the pairing and the two accessors; data access and iteration
// are not implemented yet
template <pyre::grid::concepts::PackingStrategy P, pyre::grid::concepts::StorageStrategy S>
class pyre::grid::Grid {
    // types
public:
    // my parts
    using packing_type = P;
    using storage_type = S;

    // the cell vocabulary is whatever my storage says it is
    using value_type = typename S::value_type;
    using pointer = typename S::pointer;
    using const_pointer = typename S::const_pointer;
    using reference = typename S::reference;
    using const_reference = typename S::const_reference;

    // metamethods
public:
    // constructors
    // take ownership of two strategies the caller has already built
    constexpr Grid(packing_type packing, storage_type storage);

    // build both strategies here, from the argument tuples the caller supplies, so that
    // neither one has to be movable or copyable
    template <class... PArgs, class... SArgs>
        requires(
            pyre::grid::concepts::PackingConstructible<P, PArgs...>
            && pyre::grid::concepts::StorageConstructible<S, SArgs...>)
    constexpr Grid(
        std::piecewise_construct_t, std::tuple<PArgs...> pArgs, std::tuple<SArgs...> sArgs);

    // default metamethods
public:
    // destructor
    ~Grid() = default;
    // copy/move; whether these are viable is decided by my two strategies
    Grid(const Grid &) = default;
    Grid(Grid &&) noexcept = default;
    auto operator=(const Grid &) -> Grid & = default;
    auto operator=(Grid &&) noexcept -> Grid & = default;

    // disabled metamethods
private:
    // constructors
    // there is no sensible default packing or storage, so a grid must always be told both
    Grid() = delete;

    // accessors
public:
    // how my index space maps onto memory
    [[nodiscard]] constexpr auto packing() const noexcept -> const packing_type &;
    // where my cells live
    [[nodiscard]] constexpr auto storage() const noexcept -> const storage_type &;

    // implementation details - data
private:
    // my addressing scheme
    packing_type _packing;
    // and my cells
    storage_type _storage;
};


// the inline implementations
#include "Grid.icc"


// end of file
