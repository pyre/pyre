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


// a dataset access property list
class pyre::h5::properties::DAPL : public pyre::h5::properties::List {
    // metamethods
public:
    // make a fresh dataset access property list
    DAPL();
    // the full set of special members
    DAPL(const DAPL &) = default;
    DAPL(DAPL &&) noexcept = default;
    DAPL & operator=(const DAPL &) = default;
    DAPL & operator=(DAPL &&) noexcept = default;
    ~DAPL() override = default;

    // static interface
public:
    // the shared default dataset access property list
    static auto theDefault() -> const DAPL &;

    // interface
public:
    // the chunk cache parameters: (slots, bytes, preemption policy)
    auto chunkCache() const -> std::tuple<std::size_t, std::size_t, double>;
    // set the chunk cache parameters
    auto setChunkCache(std::size_t slots, std::size_t bytes, double w0) -> void;

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit DAPL(id_type id);
};


// end of file
