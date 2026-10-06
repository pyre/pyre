// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// selectors
namespace pyre::flow::factories::selectors {
    // complex parts
    template <class signalT, class amplitudeT>
    using amplitude_t = Amplitude<signalT, amplitudeT>;

    template <class signalT, class imaginaryT>
    using imaginary_t = Imaginary<signalT, imaginaryT>;

    template <class signalT, class phaseT>
    using phase_t = Phase<signalT, phaseT>;

    template <class signalT, class realT>
    using real_t = Real<signalT, realT>;
} // namespace pyre::flow::factories::selectors


// end of file
