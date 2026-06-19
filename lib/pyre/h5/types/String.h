// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Atom.h"


// an hdf5 string datatype
class pyre::h5::types::String : public pyre::h5::types::Atom {
    // types
public:
    // the character set of my contents
    using cset_type = H5T_cset_t;
    // the padding strategy for my contents
    using strpad_type = H5T_str_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit String(id_type id);
    // make an independent copy of a predefined string type
    explicit String(const Predefined & type);
    // make a native c-style string of the given number of {cells}
    String(int, std::size_t cells);
    // the full set of special members
    String(const String &) = default;
    String(String &&) noexcept = default;
    String & operator=(const String &) = default;
    String & operator=(String &&) noexcept = default;
    ~String() override = default;

    // interface
public:
    // my character set
    auto charset() const -> cset_type;
    // set my character set
    auto setCset(cset_type cset) -> void;
    // my padding strategy
    auto strpad() const -> strpad_type;
    // set my padding strategy
    auto setStrpad(strpad_type strpad) -> void;
};


// end of file
