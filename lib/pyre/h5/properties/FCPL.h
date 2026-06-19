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


// a file creation property list
class pyre::h5::properties::FCPL : public pyre::h5::properties::List {
    // metamethods
public:
    // make a fresh file creation property list
    FCPL();
    // the full set of special members
    FCPL(const FCPL &) = default;
    FCPL(FCPL &&) noexcept = default;
    FCPL & operator=(const FCPL &) = default;
    FCPL & operator=(FCPL &&) noexcept = default;
    ~FCPL() override = default;

    // static interface
public:
    // the shared default file creation property list
    static auto theDefault() -> const FCPL &;

    // interface
public:
    // the file space page size
    auto pageSize() const -> hsize_t;
    // set the file space page size
    auto setPageSize(hsize_t size) -> void;
    // the file space strategy: (strategy, persist free space, threshold)
    auto filespaceStrategy() const -> std::tuple<H5F_fspace_strategy_t, hbool_t, hsize_t>;
    // set the file space strategy
    auto setFilespaceStrategy(H5F_fspace_strategy_t strategy, hbool_t persist, hsize_t threshold)
        -> void;

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit FCPL(id_type id);
};


// end of file
