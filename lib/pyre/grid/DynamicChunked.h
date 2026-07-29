// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// dependencies
#include "DynamicIndexIterator.h"
#include "DynamicCanonical.h"


// runtime-rank chunked packing strategy: the same tiling isomorphism as {Chunked<Rank>} but
// with the rank determined at construction time, for use in Python bindings and other dynamic
// contexts
//
// the index box is diced into tiles of a fixed extent, each stored contiguously as a unit; the
// map is the composition of two runtime-rank canonical layouts: an outer one that packs the
// grid of tiles, and an inner one that packs the interior of a single tile; there is no global
// stride vector, so this packing cannot travel as raw memory, but clients that move data in
// bulk get to work one contiguous tile at a time
// every tile occupies a full tile's worth of storage: a box whose extent is not a whole number
// of tiles is covered by letting the edge tiles run past it, and the overhang is padding that
// no index ever addresses; this makes {offset} total but not invertible
class pyre::grid::DynamicChunked {
    // types
public:
    // me
    using self_type = DynamicChunked;
    // scalars
    using size_type = size_t;
    using difference_type = std::ptrdiff_t;
    // runtime containers for each axis attribute
    using shape_type = std::vector<difference_type>;
    using index_type = std::vector<difference_type>;
    using order_type = std::vector<size_type>;
    // the nested layouts, and the shape a tile takes when it travels on its own
    using canonical_type = DynamicCanonical;
    // iterator
    using iterator_type = DynamicIndexIterator;

    // metamethods
public:
    // construct from the extent of the box and the extent of one tile (zero origin, c-style
    // order)
    DynamicChunked(const shape_type &, const shape_type &);
    // construct from the extents and the placement of the box (c-style order)
    DynamicChunked(const shape_type &, const shape_type &, const index_type &);
    // full specification: the traversal order is shared by the grid of tiles and the interior
    // of each tile
    DynamicChunked(const shape_type &, const shape_type &, const index_type &, const order_type &);

    // default special members
public:
    ~DynamicChunked() = default;
    DynamicChunked(const DynamicChunked &) = default;
    DynamicChunked(DynamicChunked &&) = default;
    auto operator=(const DynamicChunked &) -> DynamicChunked & = default;
    auto operator=(DynamicChunked &&) -> DynamicChunked & = default;

    // accessors
public:
    // the number of axes; a runtime property here, unlike in {Chunked} where it is a
    // compile-time constant
    [[nodiscard]] auto rank() const noexcept -> size_type;
    // the extent of the index box along each axis
    [[nodiscard]] auto shape() const noexcept -> const shape_type &;
    // the smallest addressable index
    [[nodiscard]] auto origin() const noexcept -> const index_type &;
    // the traversal order shared by the tile grid and the tile interiors
    [[nodiscard]] auto order() const noexcept -> const order_type &;
    // the number of cells a storage strategy must supply: every tile at full size, so this
    // includes the padding of the tiles that overhang the edges of the box
    [[nodiscard]] auto cells() const noexcept -> difference_type;

    // packing map
public:
    // the offset in memory of the cell at the given index: a full tile's worth of storage for
    // every tile packed before the one the index falls in, plus the cell's place within it
    [[nodiscard]] auto offset(const index_type &) const -> difference_type;
    // syntactic sugar
    [[nodiscard]] auto operator[](const index_type &) const -> difference_type;

    // iteration: visit every index in the box
    // the sweep covers the box in index order, not in packing order: consecutive indices need
    // not land on consecutive offsets, and the padding is never visited
public:
    // a cursor at the origin that visits every index one cell at a time
    [[nodiscard]] auto begin() const -> iterator_type;
    // a cursor at the origin that advances by the given step along each axis
    [[nodiscard]] auto begin(const index_type &) const -> iterator_type;
    // the cursor that marks the end of the traversal
    [[nodiscard]] auto end() const -> iterator_type;

    // tiling interface
public:
    // the extent of one tile
    [[nodiscard]] auto tileShape() const noexcept -> const shape_type &;
    // the extent of the grid of tiles
    [[nodiscard]] auto tiles() const noexcept -> const shape_type &;
    // the coordinates, in the grid of tiles, of the tile a given index falls in
    [[nodiscard]] auto tileOf(const index_type &) const -> index_type;
    // the rank a tile occupies in the packing sequence, which is how storage refers to it
    [[nodiscard]] auto tileOrdinal(const index_type &) const -> difference_type;
    // the layout of one tile, anchored at the tile's own corner of my index space; this is
    // what lets a tile travel as a self-contained contiguous grid over its slab of storage
    [[nodiscard]] auto tile(const index_type &) const -> canonical_type;

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
    // build the c-style permutation for a grid with the given number of axes
    static auto _defaultOrder(size_type) -> order_type;
    // the extent of the tile grid: enough tiles along each axis to cover the box
    static auto _initTiles(const shape_type &, const shape_type &) -> shape_type;
};


// get the inline implementations
#include "DynamicChunked.icc"


// end of file
