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
    // myself
    using self_type = Grid<P, S>;
    // my parts
    using packing_type = P;
    using storage_type = S;

    // i address my cells the way my packing does
    using index_type = typename P::index_type;
    using shape_type = typename P::shape_type;
    using size_type = typename P::size_type;
    using difference_type = typename P::difference_type;

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

    // the address of my first cell, for handing off to code that speaks raw memory; available
    // only when my storage keeps its cells in one expanse
    [[nodiscard]] constexpr auto data() const noexcept
        requires concepts::ContiguousStorage<storage_type>;

    // interface: reaching a cell
    // a grid is a handle to its two strategies, so reading and writing cells leaves the grid
    // itself untouched; whether the caller may write through the reference is settled by the
    // storage, whose cell type carries its own constness
public:
    // the cell named by an index, trusting the caller to stay in bounds
    [[nodiscard]] constexpr auto operator[](const index_type & idx) const -> reference;
    // the cell at a given offset, same trust
    [[nodiscard]] constexpr auto operator[](difference_type off) const -> reference;

    // the cell named by an index, with a guard against reaching past my cells
    [[nodiscard]] constexpr auto at(const index_type & idx) const -> reference;
    // the cell at a given offset, likewise guarded
    [[nodiscard]] constexpr auto at(difference_type off) const -> reference;

    // interface: sub-grids
    // both of these hand back a grid over my own cells: the derived packing inherits my physical
    // layout, so the new grid addresses my memory rather than a copy of it
    // they exist only when my packing knows how to derive a sub-layout, which is why each one
    // carries its own requirement rather than leaning on the packing contract
public:
    // the sub-grid anchored at the given index with the given extent
    [[nodiscard]] constexpr auto box(index_type base, shape_type tile) const -> self_type
        requires requires(const packing_type p, index_type i, shape_type s) { p.box(i, s); };

    // the lower rank grid that survives pinning every axis not named in {FreeAxes} at {base}
    template <std::size_t... FreeAxes>
    [[nodiscard]] constexpr auto slice(const index_type & base) const;

    // interface: iteration
    // visiting my cells in the order my packing prescribes
    // there is only one cursor type: whether a caller may write through it was settled by my
    // storage, so a const flavor would differ from this one in name only
public:
    // the cursor that walks my cells
    using iterator = GridIterator<self_type>;

    // a cursor parked on my first cell
    [[nodiscard]] constexpr auto begin() const -> iterator;
    // one that advances by the given step along each axis
    [[nodiscard]] constexpr auto begin(const index_type & step) const -> iterator;
    // and the cursor that marks the end of the sweep
    [[nodiscard]] constexpr auto end() const -> iterator;

    // implementation details - data
private:
    // my addressing scheme
    packing_type _packing;
    // and my storage strategy
    storage_type _storage;
};


// the inline implementations
#include "Grid.icc"


// end of file
