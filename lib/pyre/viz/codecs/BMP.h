// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_codecs_BMP_h)
#define pyre_viz_codecs_BMP_h


class pyre::viz::BMP {
    // type aliases
public:
    // aliases from package level
    using byte_type = byte_t;
    using color_type = color_t;
    using rgb_type = rgb_t;
    // my data buffer
    using buffer_type = byte_type *;

    // metamethods
public:
    // destructor
    inline ~BMP();
    // constructor
    inline BMP(int height, int width);
    // move
    inline BMP(BMP &&);
    inline BMP & operator=(BMP &&);

    // accessors
public:
    // the total size of the bitmap
    inline auto bytes() const -> int;
    // access to the payload
    inline auto data() const -> buffer_type;

    // interface
public:
    // encode a data stream into my payload
    template <class iteratorT>
    inline auto encode(iteratorT & source, bool topdown = true) const -> buffer_type;

    // implementation details
private:
    // data
    int _width;
    int _height;
    int _padBytesPerLine;
    int _payloadSz;
    int _bitmapSz;
    // my data buffer
    buffer_type _data;

    // constants known at compile time
    static constexpr int _fileHeaderSz = 14;
    static constexpr int _infoHeaderSz = 40;
    static constexpr int _bitPlanes = 24;
    static constexpr int _payloadOffset = _fileHeaderSz + _infoHeaderSz;
    static constexpr int _pixelSz = 3 * sizeof(byte_type);

    // disabled metamethods
public:
    // constructors
    BMP(const BMP &) = delete;
    BMP & operator=(const BMP &) = delete;
};

// get the inline definitions
#define pyre_viz_codecs_BMP_icc
#include "BMP.icc"
#undef pyre_viz_codecs_BMP_icc


#endif

// end of file
