// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

class pyre::viz::products::images::BMP : public pyre::flow::product_t {
    // type aliases
public:
    // my shape
    using shape_type = pyre::grid::shape_t<2, int>;
    // my cell type
    using cell_type = byte_t;
    // access to my data buffer
    using view_type = pyre::memory::view_t<cell_type>;
    using constview_type = pyre::memory::constview_t<cell_type>;
    // shared pointers to my instances
    using ref_type = std::shared_ptr<BMP>;

    // factory
public:
    inline static auto create(
        const name_type & name = "", shape_type shape = shape_type { 512, 512 },
        bool topdown = true) -> ref_type;

    // metamethods
public:
    // destructor
    virtual ~BMP();
    // constructor: DON'T CALL
    inline BMP(sentinel_type, const name_type &, shape_type, bool);

    // accessors
public:
    inline auto shape() const -> shape_type;
    inline auto padding() const -> int;

    // interface
public:
    // access to my data
    inline auto read() -> constview_type;
    inline auto write() -> view_type;
    // debugging support
    auto dump() -> ref_type;

    // implementation details
private:
    // data
    // the bitmap shape
    shape_type _shape;
    // file layout
    int _topdown;
    int _padBytesPerLine;
    int _payloadSz;
    int _bitmapSz;
    // the data buffer
    cell_type * _data;

    // constants known at compile time
    static constexpr int _fileHeaderSz = 14;
    static constexpr int _infoHeaderSz = 40;
    static constexpr int _payloadOffset = _fileHeaderSz + _infoHeaderSz;
    static constexpr int _pixelSz = 3 * sizeof(cell_type);
    static constexpr int _bitsPerPixel = 8 * _pixelSz;

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