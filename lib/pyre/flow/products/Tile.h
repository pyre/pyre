// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

template <class gridT>
class pyre::flow::products::Tile : public pyre::flow::product_t {
    // type aliases
public:
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

    // factory
public:
    inline static auto create(const name_type & name, shape_type shape, cell_type value = 0)
        -> ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Tile();
    // constructor; DON'T CALL
    inline Tile(sentinel_type, const name_type &, shape_type, cell_type);

    // accessors
public:
    inline auto shape() const -> shape_type;

    // mutators
public:
    inline auto value(cell_type) -> void;

    // interface
public:
    // value access by factories
    inline auto read() -> const grid_type &;
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
