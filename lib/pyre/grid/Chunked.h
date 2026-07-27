// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// dependencies
#include "Shape.h"
#include "Index.h"
#include "Order.h"
#include "IndexIterator.h"
#include "Canonical.h"


// the chunked packing strategy: the index box is diced into tiles of a fixed extent, and each
// tile is stored contiguously as a unit
// the map is the composition of two canonical layouts: an outer one that packs the grid of
// tiles, and an inner one that packs the interior of a single tile; there is no global stride
// vector, so this packing cannot travel as raw memory, but clients that move data in bulk get
// to work one contiguous tile at a time
// every tile occupies a full tile's worth of storage: a box whose extent is not a whole number
// of tiles is covered by letting the edge tiles run past it, and the overhang is padding that
// no index ever addresses; this makes {offset} total but not invertible
template <std::size_t Rank>
class pyre::grid::Chunked {
    // types
public:
    // myself
    using self_type = Chunked<Rank>;
    // parts
    using index_type = Index<Rank>;
    using shape_type = Shape<Rank>;
    using order_type = Order<Rank>;
    // the two nested layouts
    using canonical_type = Canonical<Rank>;
    // scalars
    using size_type = size_t;
    using difference_type = std::ptrdiff_t;
    // iterator
    using iterator_type = IndexIterator<Rank>;

    // metamethods
public:
    // primary constructor: the extent of the box, the extent of one tile, and the placement;
    // the traversal order is shared by the grid of tiles and the interior of each tile
    constexpr Chunked(
        const shape_type &, const shape_type &, const index_type & = index_type::zero(),
        const order_type & = order_type::c()) noexcept;

    // default metamethods
public:
    // destructor
    ~Chunked() = default;
    // a layout is a value: it copies and moves freely
    Chunked(const Chunked &) = default;
    Chunked(Chunked &&) = default;
    auto operator=(const Chunked &) noexcept -> self_type & = default;
    auto operator=(Chunked &&) noexcept -> self_type & = default;

    // accessors
public:
    // the extent of the index box along each axis
    [[nodiscard]] constexpr auto shape() const noexcept -> shape_type;
    // the smallest addressable index
    [[nodiscard]] constexpr auto origin() const noexcept -> index_type;
    // the traversal order shared by the tile grid and the tile interiors
    [[nodiscard]] constexpr auto order() const noexcept -> order_type;
    // the number of cells a storage strategy must supply: every tile at full size, so this
    // includes the padding of the tiles that overhang the edges of the box
    [[nodiscard]] constexpr auto cells() const noexcept -> difference_type;
    // my rank, as a compile time constant
    static consteval auto rank() noexcept -> size_type;

    // packing map
public:
    // the offset in memory of the cell at the given index: a full tile's worth of storage for
    // every tile packed before the one the index falls in, plus the cell's place within it
    [[nodiscard]] constexpr auto offset(const index_type &) const noexcept -> difference_type;
    // syntactic sugar
    [[nodiscard]] constexpr auto operator[](const index_type &) const noexcept -> difference_type;

    // iteration: visit every index in the box
    // the sweep covers the box in index order, not in packing order: consecutive indices need
    // not land on consecutive offsets, and the padding is never visited
public:
    // a cursor at {origin} that visits every index one cell at a time
    [[nodiscard]] constexpr auto begin() const noexcept -> iterator_type;
    // a cursor at {origin} that advances by the given step along each axis
    [[nodiscard]] constexpr auto begin(const index_type &) const noexcept -> iterator_type;
    // the cursor that marks the end of the traversal
    [[nodiscard]] constexpr auto end() const noexcept -> iterator_type;

    // tiling interface
public:
    // the extent of one tile
    [[nodiscard]] constexpr auto tileShape() const noexcept -> shape_type;
    // the extent of the grid of tiles
    [[nodiscard]] constexpr auto tiles() const noexcept -> shape_type;
    // the coordinates, in the grid of tiles, of the tile a given index falls in
    [[nodiscard]] constexpr auto tileOf(const index_type &) const noexcept -> index_type;
    // the rank a tile occupies in the packing sequence, which is how storage refers to it
    [[nodiscard]] constexpr auto tileOrdinal(const index_type &) const noexcept -> difference_type;
    // the layout of one tile, anchored at the tile's own corner of my index space; this is
    // what lets a tile travel as a self-contained contiguous grid over its slab of storage
    [[nodiscard]] constexpr auto tile(const index_type &) const noexcept -> canonical_type;

    // implementation details
private:
    // the extent of the box; not deducible from the nested layouts, whose edge tiles overhang it
    shape_type _shape {};
    // the smallest addressable index; may be negative
    index_type _origin {};
    // the layout of the grid of tiles, anchored at zero
    canonical_type _outer;
    // the layout of the interior of one tile, anchored at zero
    canonical_type _inner;

    // static helpers
private:
    // the extent of the tile grid: enough tiles along each axis to cover the box
    static constexpr auto _initTiles(const shape_type &, const shape_type &) noexcept -> shape_type;
};


// get the inline implementations
#include "Chunked.icc"


// end of file
