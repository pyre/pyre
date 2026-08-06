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
// the values my settings trade in
#include "FilespaceStrategy.h"
#include "Sizes.h"


// a file creation property list
class pyre::h5::properties::FCPL : public pyre::h5::properties::List {
    // metamethods
public:
    // me
    using self_type = FCPL;
    // my superclass
    using super_type = pyre::h5::properties::List;
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
    auto pageSize(hsize_t size) -> void;
    // the size of the user block, a byte range at the front of the file that hdf5 leaves
    // alone, so another format can carry an hdf5 product inside itself
    auto userblock() const -> hsize_t;
    // set the size of the user block
    auto userblock(hsize_t size) -> void;
    // the widths hdf5 uses to record positions and lengths, as (offset bytes, length bytes)
    auto sizes() const -> Sizes;
    // set the widths used to record positions and lengths
    auto sizes(const Sizes & sizes) -> void;
    // the file space strategy: (strategy, persist free space, threshold)
    auto filespaceStrategy() const -> FilespaceStrategy;
    // set the file space strategy
    auto filespaceStrategy(const FilespaceStrategy & strategy) -> void;

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit FCPL(id_type id);
};


// end of file
