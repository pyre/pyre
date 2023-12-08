// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::viz::products::BMP : public pyre::flow::product_t {
    // type aliases
public:
    // my shape
    using shape_type = std::tuple<int, int>;
    // my cell type
    using cell_type = unsigned char;
    // access to my data buffer
    using view_type = pyre::memory::view_t<cell_type>;
    using constview_type = pyre::memory::constview_t<cell_type>;
    // shared pointers to my instances
    using ref_type = std::shared_ptr<BMP>;

    // factory
public:
    inline static auto create(shape_type = shape_type { 512, 512 }) -> ref_type;

    // metamethods
public:
    // destructor
    virtual ~BMP();
    // constructor: DON'T CALL
    inline BMP(sentinel_type, shape_type);

private:
    // accessors
public:
    inline auto shape() const -> shape_type;
    inline auto data() const -> constview_type;

    // mutators
public:
    inline auto shape(shape_type) -> void;
    inline auto data() -> view_type;

    // interface
public:
    // build a reference to me
    inline auto ref() -> ref_type;
    // invalidate me
    virtual auto flush() -> void override;
    // debugging support
    auto dump() const -> void;

    // implementation details - data
protected:
    shape_type _shape;
    cell_type * _data;

    // metamethods
private:
    // suppressed constructors
    BMP(const BMP &) = delete;
    BMP & operator=(const BMP &) = delete;
    BMP(BMP &&) = delete;
    BMP & operator=(BMP &&) = delete;
};

// get the inline definitions
#include "BMP.icc"

// end of file