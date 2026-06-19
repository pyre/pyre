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


// a predefined hdf5 datatype, e.g. one of the {H5T_NATIVE_*} or {H5T_STD_*} constants
class pyre::h5::types::Predefined : public pyre::h5::types::Atom {
    // metamethods
public:
    // wrap a predefined-type constant, sharing the reference the library owns forever
    explicit Predefined(id_type id);
    // the full set of special members
    Predefined(const Predefined &) = default;
    Predefined(Predefined &&) noexcept = default;
    Predefined & operator=(const Predefined &) = default;
    Predefined & operator=(Predefined &&) noexcept = default;
    ~Predefined() override = default;
};


// end of file
