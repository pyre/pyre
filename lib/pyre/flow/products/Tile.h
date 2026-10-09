// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "../protocols/Product.h"

// a product that holds a tile of cells in a grid; tiles are packed in row major order, the c
// convention, and the factories that read and write them rely on it: they walk the cells of a tile
// in memory order, and expect the cells of a line next to each other
template <class gridT>
class pyre::flow::products::Tile : public pyre::flow::protocols::Product {
    // type aliases
public:
    // me
    using self_type = Tile<gridT>;
    // my superclass
    using super_type = pyre::flow::protocols::Product;
    // my template parameter
    using grid_type = gridT;
    // the packing strategy
    using packing_type = typename grid_type::packing_type;
    // the storage strategy
    using storage_type = typename grid_type::storage_type;
    // my cell type
    using cell_type = typename storage_type::value_type;
    // shape
    using shape_type = typename packing_type::shape_type;

    // shared pointers to my instances
    using ref_type = std::shared_ptr<Tile>;
    // the spelling of types
    using string_type = string_t;

    // the spelling of my type
public:
    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // the human readable form of my class name
    static inline auto className() -> string_type;

    // factory
public:
    // make a tile whose cells are left uninitialized, so it starts stale
    inline static auto create(const name_type & name, shape_type shape) -> ref_type;
    // make a tile with every cell set to {value}, so it starts fresh
    inline static auto create(const name_type & name, shape_type shape, cell_type value)
        -> ref_type;
    // make a tile over the cells of {grid}, which it shares rather than copies, so it starts
    // fresh; this is how a raster that lives elsewhere, such as a memory mapped file, enters a
    // graph
    inline static auto create(const name_type & name, grid_type grid) -> ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Tile();
    // constructors; DON'T CALL
    inline Tile(sentinel_type, const name_type &, shape_type);
    inline Tile(sentinel_type, const name_type &, shape_type, cell_type);
    inline Tile(sentinel_type, const name_type &, grid_type);

    // accessors
public:
    inline auto shape() const -> shape_type;

    // mutators
public:
    inline auto value(cell_type) -> void;

    // interface
public:
    // my cells, refreshed first if i am stale
    inline auto read() -> const grid_type &;
    // my cells, for writing; whatever is computed from them is marked stale right away
    inline auto write() -> grid_type &;

    // implementation details - data
private:
    // the data buffer
    grid_type _data;

    // metamethods
private:
    // suppressed constructors
    Tile(const Tile &) = delete;
    Tile & operator=(const Tile &) = delete;
    Tile(Tile &&) = delete;
    Tile & operator=(Tile &&) = delete;
};

// get the inline definitions
#include "Tile.icc"


// end of file
