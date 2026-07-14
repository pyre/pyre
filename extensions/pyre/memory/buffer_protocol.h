// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::memory {
    // add support for the python buffer protocol
    template <class memT>
    void bindBufferProtocol(shared_holder_t<memT> &);

} // namespace pyre::py::memory


// get the inline definitions
#include "buffer_protocol.icc"


// end of file
