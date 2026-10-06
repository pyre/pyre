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
namespace pyre::viz::iterators::filters {
    // a filter that adds two others
    template <class op1T, class op2T>
    using add_t = Add<op1T, op2T>;
    // map a [0,1] interval into a portion of an interval
    template <class sourceT>
    using affine_t = Affine<sourceT>;
    // extract the amplitude of a complex dataset
    template <class sourceT>
    using amplitude_t = Amplitude<sourceT>;
    // supply a constant value
    template <typename valueT = double>
    using constant_t = Constant<valueT>;
    // compute phase as a cycle in [0,1]
    template <typename valueT = double>
    using cycle_t = Cycle<valueT>;
    // a simple compressor that just drops pixels
    template <class sourceT>
    using decimate_t = Decimate<sourceT>;
    // a filter that maps values in [0,1] to the index of of a call in a geometrically spaced grid
    template <class sourceT>
    using geometric_t = Geometric<sourceT>;
    // extract the imaginary part of a complex dataset
    template <class sourceT>
    using imaginary_t = Imaginary<sourceT>;
    // a saw tooth function on the log of its input value
    template <class sourceT>
    using logsaw_t = LogSaw<sourceT>;
    // a filter that multiplies two others
    template <class op1T, class op2T>
    using mul_t = Multiply<op1T, op2T>;
    // scale values relative to a given interval
    template <class sourceT>
    using parametric_t = Parametric<sourceT>;
    // extract the phase of a complex dataset
    template <class sourceT>
    using phase_t = Phase<sourceT>;
    // a saw tooth function on the phase of its input value
    template <class sourceT>
    using polarsaw_t = PolarSaw<sourceT>;
    // a power law filter for signal amplitudes
    template <class sourceT>
    using power_t = Power<sourceT>;
    // extract the real part of a complex dataset
    template <class sourceT>
    using real_t = Real<sourceT>;
    // a saw tooth function on the phase of its input value
    // a filter that maps values in [0,1] to the index of of a call in a uniformly spaced grid
    template <class sourceT>
    using uniform_t = Uniform<sourceT>;
} // namespace pyre::viz::iterators::filters


// end of file
