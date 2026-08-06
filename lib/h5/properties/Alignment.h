// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// where the objects in a file start
// hdf5 starts any object at least {threshold} bytes long on a multiple of {boundary};
// the two travel together because neither says anything on its own
class pyre::h5::properties::Alignment {
    // types
public:
    // me
    using self_type = Alignment;

    // metamethods
public:
    // describe where the objects in a file start
    Alignment(hsize_t threshold, hsize_t boundary);
    // the full set of special members
    Alignment(const Alignment &) = default;
    Alignment(Alignment &&) noexcept = default;
    Alignment & operator=(const Alignment &) = default;
    Alignment & operator=(Alignment &&) noexcept = default;
    ~Alignment() = default;

    // data
public:
    // the size an object must reach before it is placed deliberately
    hsize_t threshold;
    // the multiple such an object starts on
    hsize_t boundary;
};


// the inline definitions
#include "Alignment.icc"


// end of file
