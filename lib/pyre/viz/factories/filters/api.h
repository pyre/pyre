// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// filters
namespace pyre::viz::factories::filters {
    // map [0,1] onto [a,b]
    template <class signalT, class affineT>
    using affine_t = Affine<signalT, affineT>;

    // a filter that maps the phase of its complex source to [0,1]
    template <class signalT, class cycleT>
    using cycle_t = Cycle<signalT, cycleT>;

    // generate a tile filled with a constant
    template <class constantT>
    using constant_t = Constant<constantT>;

    // zoom by a factor of 2
    template <class signalT>
    using decimate_t = Decimate<signalT>;

    // map values in [0,1] into geometrically spaced bins
    template <class signalT, class binT>
    using geometric_t = Geometric<signalT, binT>;

    // map the log of the absolute value of the signal to [0,1]
    // works on both real and complex data
    template <class signalT, class logsawT>
    using logsaw_t = LogSaw<signalT, logsawT>;

    // map values in [a,b] to [0,1]
    template <class signalT, class binT>
    using parametric_t = Parametric<signalT, binT>;

    // map phase to [0,1]
    // works on both real and complex data
    template <class signalT, class polarsawT>
    using polarsaw_t = PolarSaw<signalT, polarsawT>;

    // map signal to scale * (signal/mean)^exponent
    template <class signalT, class powerT>
    using power_t = Power<signalT, powerT>;

    // map values in [0,1] into uniformly spaced bins
    template <class signalT, class binT>
    using uniform_t = Uniform<signalT, binT>;
} // namespace pyre::viz::factories::filters


// end of file
