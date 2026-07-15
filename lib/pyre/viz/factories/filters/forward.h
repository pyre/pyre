// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "../../forward.h"


// forward declarations
namespace pyre::viz::factories::filters {
    template <class signalT, class affineT>
    class Affine;
    template <class signalT, class cycleT>
    class Cycle;
    template <class constantT>
    class Constant;
    template <class signalT>
    class Decimate;
    template <class signalT, class binT>
    class Geometric;
    template <class signalT, class logsawT>
    class LogSaw;
    template <class signalT, class parametricT>
    class Parametric;
    template <class signalT, class polarsawT>
    class PolarSaw;
    template <class signalT, class powerT>
    class Power;
    template <class signalT, class binT>
    class Uniform;
} // namespace pyre::viz::factories::filters


// end of file
