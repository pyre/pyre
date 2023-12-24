// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::viz::products::memory::TileF4 : public pyre::flow::product_t {
    // type aliases
public:
    // my cell type
    using cell_type = pyre::viz::f4_t;
    // shape
    using shape_type = pyre::grid::shape_t<2>;
    // packing strategy
    using packing_type = pyre::grid::canonical_t<2>;
    // memory strategy
    using memory_type = pyre::memory::heap_t<cell_type>;
    // memory
    using grid_type = pyre::grid::grid_t<packing_type, memory_type>;
    // and shared pointers to my instances
    using ref_type = std::shared_ptr<TileF4>;

    // factory
public:
    inline static auto create(const name_type & name, shape_type shape, cell_type value = 0)
        -> ref_type;

    // metamethods
public:
    // destructor
    virtual ~TileF4();
    // constructor; DON'T CALL
    inline TileF4(sentinel_type, const name_type &, shape_type, cell_type);

    // accessors
public:
    inline auto shape() const -> shape_type;

    // interface
public:
    // value access by factories
    inline auto read() -> const grid_type &;
    inline auto write() -> grid_type &;

    // implementation details - data
private:
    // my shape
    shape_type _shape;
    // and the data buffer
    grid_type _data;

    // metamethods
private:
    // suppressed constructors
    TileF4(const TileF4 &) = delete;
    TileF4 & operator=(const TileF4 &) = delete;
    TileF4(TileF4 &&) = delete;
    TileF4 & operator=(TileF4 &&) = delete;
};

// get the inline definitions
#include "TileF4.icc"

// end of file
