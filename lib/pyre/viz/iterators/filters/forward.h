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
namespace pyre::viz::iterators::filters {
    // a filter that adds two others
    template <class op1T, class op2T>
    class Add;
    // map [0,1] to a portion of an interval
    template <class sourceT>
    class Affine;
    // extract the amplitude of a complex source
    template <class sourceT>
    class Amplitude;
    // supply a constant value
    template <typename valueT>
    class Constant;
    // compute phase as a cycle in [0,1]
    template <typename valueT>
    class Cycle;
    // a simple compressor that just drops pixels
    template <class sourceT>
    class Decimate;
    // a filter that maps values in [0,1] to the index of of a call in a geometrically
    // spaced grid
    template <class sourceT>
    class Geometric;
    // imaginary part of a complex source
    template <class sourceT>
    class Imaginary;
    // a saw tooth function based on the log of its input value
    template <class sourceT>
    class LogSaw;
    // a filter that multiples two others
    template <class op1T, class op2T>
    class Multiply;
    // scale values relative to an interval
    template <class sourceT>
    class Parametric;
    // extract the phase of a complex source
    template <class sourceT>
    class Phase;
    // a saw tooth function based on the phase of its input value
    template <class sourceT>
    class PolarSaw;
    // a power law filter for amplitudes
    template <class sourceT>
    class Power;
    // real part of a complex source
    template <class sourceT>
    class Real;
    // a filter that maps values in [0,1] to the index of of a call in a uniformly spaced
    // grid
    template <class sourceT>
    class Uniform;
} // namespace pyre::viz::iterators::filters


// end of file
