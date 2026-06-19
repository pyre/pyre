// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Datatype.h"


// an hdf5 array datatype
class pyre::h5::types::Array : public pyre::h5::types::Datatype {
    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit Array(id_type id);
    // make an array of the given {cell} type and {shape}
    Array(const Datatype & cell, const shape_t & shape);
    // the full set of special members
    Array(const Array &) = default;
    Array(Array &&) noexcept = default;
    Array & operator=(const Array &) = default;
    Array & operator=(Array &&) noexcept = default;
    ~Array() override = default;
};


// end of file
