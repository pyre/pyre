// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::viz::products::memory::TileC8 : public pyre::flow::product_t {
    // type aliases
public:
    // my cell type
    using cell_type = pyre::viz::c8_t;
    // shape
    using shape_type = pyre::grid::shape_t<2>;
    // packing strategy
    using packing_type = pyre::grid::canonical_t<2>;
    // memory strategy
    using memory_type = pyre::memory::heap_t<cell_type>;
    // memory
    using grid_type = pyre::grid::grid_t<packing_type, memory_type>;
    // and shared pointers to my instances
    using ref_type = std::shared_ptr<TileC8>;

    // factory
public:
    inline static auto create(shape_type shape, cell_type value = 0) -> ref_type;

    // metamethods
public:
    // destructor
    virtual ~TileC8();
    // constructor; DON'T CALL
    inline TileC8(sentinel_type, shape_type, cell_type);

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
    TileC8(const TileC8 &) = delete;
    TileC8 & operator=(const TileC8 &) = delete;
    TileC8(TileC8 &&) = delete;
    TileC8 & operator=(TileC8 &&) = delete;
};

// get the inline definitions
#include "TileC8.icc"

// end of file
