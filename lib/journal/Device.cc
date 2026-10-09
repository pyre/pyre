// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external support
#include "externals.h"
// forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// get the device declaration
#include "Device.h"


// metamethods
// destructor
pyre::journal::Device::~Device() {}


// interface
// whether i am implemented outside c++
auto
pyre::journal::Device::foreign() const -> bool
{
    // devices are native unless they say otherwise
    return false;
}


// end of file
