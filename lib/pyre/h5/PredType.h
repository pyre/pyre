// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "AtomType.h"


// a predefined hdf5 datatype, e.g. one of the {H5T_NATIVE_*} or {H5T_STD_*} constants
class pyre::h5::PredType : public pyre::h5::AtomType {
    // metamethods
public:
    // wrap a predefined-type constant, sharing the reference the library owns forever
    explicit PredType(id_type id);
    // the full set of special members
    PredType(const PredType &) = default;
    PredType(PredType &&) noexcept = default;
    PredType & operator=(const PredType &) = default;
    PredType & operator=(PredType &&) noexcept = default;
    ~PredType() override = default;
};


// end of file
