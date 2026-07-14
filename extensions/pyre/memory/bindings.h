// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::memory {
    // decorate a storage class with bindings that do not require write access to {memT}
    template <class memT>
    void bindConstStorage(shared_holder_t<memT> &);

    // decorate a storage class with bindings that require write access to {memT}
    template <class memT>
    void bindStorage(shared_holder_t<memT> &);

} // namespace pyre::py::memory


// get the inline definitions
#include "bindings.icc"


// end of file
