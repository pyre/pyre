// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// control over the level of detail
class pyre::journal::Detail {
    // types
public:
    // me
    using self_type = Detail;
    // the detail level
    using detail_type = detail_t;

    // metamethods
public:
    // constructor
    inline explicit Detail(detail_type);

    // interface
public:
    // accessors
    inline auto detail() const -> detail_type;

    // data
private:
    const detail_type _detail;
};


// get the inline definitions
#include "Detail.icc"


// end of file
