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


// a file access property list
class pyre::h5::properties::FAPL : public pyre::h5::properties::List {
    // metamethods
public:
    // make a fresh file access property list
    FAPL();
    // the full set of special members
    FAPL(const FAPL &) = default;
    FAPL(FAPL &&) noexcept = default;
    FAPL & operator=(const FAPL &) = default;
    FAPL & operator=(FAPL &&) noexcept = default;
    ~FAPL() override = default;

    // static interface
public:
    // the shared default file access property list
    static auto theDefault() -> const FAPL &;

    // interface
public:
    // the metadata block size
    auto metaBlockSize() const -> hsize_t;
    // set the metadata block size
    auto setMetaBlockSize(hsize_t size) -> void;
    // the page buffer characteristics: (bytes, metadata percent, raw-data percent)
    auto pageBufferSize() const -> std::tuple<std::size_t, unsigned int, unsigned int>;
    // set the page buffer characteristics
    auto setPageBufferSize(std::size_t buffer, unsigned int meta, unsigned int raw) -> void;

#if defined(H5_HAVE_ROS3_VFD)
    // configure the read-only S3 virtual file driver
    auto ros3(
        bool authenticate, string_t region, string_t id, string_t key, string_t token) -> FAPL &;
#endif

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit FAPL(id_type id);
};


// end of file
