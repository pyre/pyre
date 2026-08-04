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
#include "List.h"


// a file access property list
class pyre::h5::properties::FAPL : public pyre::h5::properties::List {
    // metamethods
public:
    // me
    using self_type = FAPL;
    // my superclass
    using super_type = pyre::h5::properties::List;
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

    // the alignment of objects in the file, as (threshold, alignment); objects at least
    // {threshold} bytes long start at a multiple of {alignment}, which is what makes reads
    // land on stripe boundaries on a parallel filesystem
    auto alignment() const -> std::tuple<hsize_t, hsize_t>;
    // set the alignment of objects in the file
    auto setAlignment(hsize_t threshold, hsize_t alignment) -> void;

    // the size of the sieve buffer, which gathers small writes to a contiguous dataset
    auto sieveBufferSize() const -> std::size_t;
    // set the size of the sieve buffer
    auto setSieveBufferSize(std::size_t size) -> void;

    // what happens to a file whose handle is closed while objects in it are still open
    auto closeDegree() const -> H5F_close_degree_t;
    // set the file close degree
    auto setCloseDegree(H5F_close_degree_t degree) -> void;

    // the default caches, as (metadata elements, chunk slots, chunk bytes, preemption
    // policy); the chunk cache settings here are the defaults that a dataset access
    // property list overrides for one dataset at a time
    auto cache() const -> std::tuple<int, std::size_t, std::size_t, double>;
    // set the default caches
    auto setCache(int elements, std::size_t slots, std::size_t bytes, double w0) -> void;

    // the bounds on the file format versions hdf5 may use, as (low, high); the newer
    // features — extendable chunk indices among them — are only available to a file that
    // is allowed to use a recent format, at the cost of who can read it afterwards
    auto libverBounds() const -> std::tuple<H5F_libver_t, H5F_libver_t>;
    // set the bounds on the file format versions
    auto setLibverBounds(H5F_libver_t low, H5F_libver_t high) -> void;

#if defined(H5_HAVE_ROS3_VFD)
    // configure the read-only S3 virtual file driver
    auto ros3(bool authenticate, string_t region, string_t id, string_t key, string_t token)
        -> FAPL &;
#endif

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit FAPL(id_type id);
};


// end of file
