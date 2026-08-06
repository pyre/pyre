// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "OCPL.h"
// the value my pipeline is made of
#include "Filter.h"


// a dataset creation property list
class pyre::h5::properties::DCPL : public pyre::h5::properties::OCPL {
    // types
public:
    // me
    using self_type = DCPL;
    // my superclass
    using super_type = pyre::h5::properties::OCPL;
    // one stage of my pipeline
    using filter_type = Filter;
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
    auto allocTime(H5D_alloc_time_t timing) -> void;
    // the fill value writing time
    auto fillTime() const -> H5D_fill_time_t;
    // set the fill value writing time
    auto fillTime(H5D_fill_time_t timing) -> void;
    // whether a fill value is defined, and how
    auto fillValueStatus() const -> H5D_fill_value_t;
    // the fill value, read into {value} as the given {type}
    auto readFillValue(const pyre::h5::types::Datatype & type, void * value) const -> void;
    // set the fill value, read from {value} as the given {type}; hdf5 converts it to the
    // dataset's on-disk type at creation
    auto fillValue(const pyre::h5::types::Datatype & type, const void * value) -> void;

    // the data layout strategy
    auto layout() const -> H5D_layout_t;
    // set the data layout strategy
    auto layout(H5D_layout_t layout) -> void;
    // the chunk shape; empty when my layout is not chunked
    auto chunk() const -> shape_t;
    // set the chunk {shape}
    auto chunk(const shape_t & shape) -> void;

    // interface: filters
public:
    // the filters in the dataset pipeline
    auto filters() const -> filters_type;
    // engage the deflate (gzip) filter at the given compression {level}
    auto addDeflate(unsigned int level) -> void;
    // engage the szip filter
    auto addSzip(unsigned int options, unsigned int pixelsPerBlock) -> void;
    // engage the n-bit filter
    auto addNbit() -> void;
    // engage the shuffle filter
    auto addShuffle() -> void;
    // engage the fletcher32 checksum filter
    auto addFletcher32() -> void;
    // engage the scale-offset filter
    auto addScaleoffset(H5Z_SO_scale_type_t scaleType, int scaleFactor) -> void;

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit DCPL(id_type id);
};


// end of file
