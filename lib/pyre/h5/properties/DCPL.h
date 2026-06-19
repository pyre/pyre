// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "List.h"


// a dataset creation property list
class pyre::h5::properties::DCPL : public pyre::h5::properties::List {
    // types
public:
    // a filter as (id, name, flags, configuration)
    using filter_type = std::tuple<H5Z_filter_t, string_t, unsigned int, unsigned int>;
    // the dataset filter pipeline
    using filters_type = std::vector<filter_type>;

    // metamethods
public:
    // make a fresh dataset creation property list
    DCPL();
    // the full set of special members
    DCPL(const DCPL &) = default;
    DCPL(DCPL &&) noexcept = default;
    DCPL & operator=(const DCPL &) = default;
    DCPL & operator=(DCPL &&) noexcept = default;
    ~DCPL() override = default;

    // static interface
public:
    // the shared default dataset creation property list
    static auto theDefault() -> const DCPL &;

    // interface: layout and timing
public:
    // the storage allocation time
    auto allocTime() const -> H5D_alloc_time_t;
    // set the storage allocation time
    auto setAllocTime(H5D_alloc_time_t timing) -> void;
    // the fill value writing time
    auto fillTime() const -> H5D_fill_time_t;
    // set the fill value writing time
    auto setFillTime(H5D_fill_time_t timing) -> void;
    // the data layout strategy
    auto layout() const -> H5D_layout_t;
    // set the data layout strategy
    auto setLayout(H5D_layout_t layout) -> void;
    // the chunk shape, given the dataset {rank}
    auto chunk(int rank) const -> shape_t;
    // set the chunk {shape}
    auto setChunk(const shape_t & shape) -> void;

    // interface: filters
public:
    // the filters in the dataset pipeline
    auto filters() const -> filters_type;
    // engage the deflate (gzip) filter at the given compression {level}
    auto setDeflate(unsigned int level) -> void;
    // engage the szip filter
    auto setSzip(unsigned int options, unsigned int pixelsPerBlock) -> void;
    // engage the n-bit filter
    auto setNbit() -> void;
    // engage the shuffle filter
    auto setShuffle() -> void;
    // engage the fletcher32 checksum filter
    auto setFletcher32() -> void;
    // engage the scale-offset filter
    auto setScaleoffset(H5Z_SO_scale_type_t scaleType, int scaleFactor) -> void;

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit DCPL(id_type id);
};


// end of file
