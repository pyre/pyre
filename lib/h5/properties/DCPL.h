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
    // declare the value that stands in for cells nobody writes; hdf5 converts it to the
    // dataset's own type when the dataset is created, so the type of {value} here is only
    // how i am handed the bytes. there is deliberately no reader to pair with this: a
    // property list cannot be asked what its fill value is, because hdf5 keeps no record
    // of the type it was declared in, and answering would mean asking the caller to name
    // one and trusting the guess. ask the dataset instead, which knows its own type
    template <class valueT>
    auto fillValue(const valueT & value) -> void;

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


// the inline definitions
#include "DCPL.icc"


// end of file
