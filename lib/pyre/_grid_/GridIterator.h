// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"

// support
#include <optional>


// iterator that visits the cells of a grid, rather than the indices that name them
// it wraps the index iterator its grid's packing hands out, and dereferences to whatever cell
// that index points at; the traversal order is therefore the packing's, not one of its own
// there is no const flavor of this iterator: a grid reaches its cells through a const interface,
// and whether the caller may write through the reference was settled by the storage, whose cell
// type carries its own constness
template <class gridT>
class pyre::grid::GridIterator {
    // types
public:
    // myself
    using self_type = GridIterator<gridT>;
    // my parts
    using grid_type = gridT;
    // the cursor that walks index space for me
    using index_iterator = typename gridT::packing_type::iterator_type;

    // iterator traits for STL compatibility
    // what a dereference yields: a cell of the grid
    using value_type = typename gridT::value_type;
    // handed out as whatever reference the storage deals in
    using reference = typename gridT::reference;
    using pointer = typename gridT::pointer;
    using difference_type = typename gridT::difference_type;
    // i can only move forward, and only one cell at a time
    using iterator_category = std::forward_iterator_tag;

    // metamethods
public:
    // singular iterator; satisfies the std::regular requirement on forward iterators
    GridIterator() = default;
    // park on the cell named by the given index cursor, in the given grid
    constexpr GridIterator(grid_type, index_iterator) noexcept;

    // default metamethods
public:
    ~GridIterator() = default;
    GridIterator(const GridIterator &) = default;
    GridIterator(GridIterator &&) noexcept = default;
    auto operator=(const GridIterator &) -> self_type & = default;
    auto operator=(GridIterator &&) noexcept -> self_type & = default;

    // iterator protocol
public:
    // hand out the cell i am parked on
    [[nodiscard]] constexpr auto operator*() const -> reference;
    // move on to the cell named by the next index in the traversal
    constexpr auto operator++() -> self_type &;
    // same, but report the cell i was parked on before i moved
    constexpr auto operator++(int) -> self_type;

    // accessors
public:
    // the index cursor i am riding, so that equality can be settled without friendship
    [[nodiscard]] constexpr auto cursor() const noexcept -> const index_iterator &;

    // implementation details
private:
    // a copy of the grid, not a reference: a grid is a lightweight handle to two strategies, so
    // owning one by value keeps me valid even when i was handed a temporary
    // it is optional only because a grid has no sensible default, while a forward iterator must
    // have a singular state; a default constructed cursor holds no grid and may not be
    // dereferenced, which is the usual contract for a singular iterator
    std::optional<grid_type> _grid {};
    // where i am in index space
    index_iterator _cursor;
};


// get the inline implementations
#include "GridIterator.icc"


// end of file
