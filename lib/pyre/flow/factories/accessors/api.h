// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the forward declarations of {pyre::flow::factories::accessors}
#include "forward.h"


// accessors
namespace pyre::flow::factories::accessors {
    // the parts of a complex value
    template <class signalT, class imaginaryT>
    using imaginary_t = Imaginary<signalT, imaginaryT>;

    template <class signalT, class realT>
    using real_t = Real<signalT, realT>;
} // namespace pyre::flow::factories::accessors


// end of file
