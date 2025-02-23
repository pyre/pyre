// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"


// the {pyre} extension namespace
namespace pyre::py::memory {
    // add support for the python buffer protocol
    template <class T>
    void bufferProtocol(shared_holder_t<T> &);
} // namespace pyre::py::memory


// get the implementation
#include "buffer_protocol.icc"


// end of file
