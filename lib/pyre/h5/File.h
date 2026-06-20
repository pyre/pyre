// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Group.h"


// an hdf5 file; its group interface operates on the root group
class pyre::h5::File : public pyre::h5::Group {
    // metamethods
public:
    // open or create the file at {uri}; {flags} chooses the access mode and whether to create
    File(
        const string_t & uri, unsigned int flags, const properties::FCPL & fcpl,
        const properties::FAPL & fapl);
    // an empty file handle, e.g. for a failed open
    File();
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit File(id_type id);
    // the full set of special members
    File(const File &) = default;
    File(File &&) noexcept = default;
    File & operator=(const File &) = default;
    File & operator=(File &&) noexcept = default;
    ~File() override = default;

    // interface
public:
    // my creation property list, as a fresh owned wrapper
    auto fcpl() const -> properties::FCPL;
    // my access property list, as a fresh owned wrapper
    auto fapl() const -> properties::FAPL;
};


// end of file
