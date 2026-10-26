// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the forward declarations of {pyre::flow::factories::operators}
#include "forward.h"


// operators
namespace pyre::flow::factories::operators {
    // the arithmetic; the result is a tile when either operand is one, and otherwise a scalar
    // addition
    template <
        class op1T, class op2T = op1T, class resultT = std::conditional_t<tile_c<op2T>, op2T, op1T>>
    using add_t = Arithmetic<std::plus<>, op1T, op2T, resultT>;

    // subtraction
    template <
        class op1T, class op2T = op1T, class resultT = std::conditional_t<tile_c<op2T>, op2T, op1T>>
    using subtract_t = Arithmetic<std::minus<>, op1T, op2T, resultT>;

    // multiplication
    template <
        class op1T, class op2T = op1T, class resultT = std::conditional_t<tile_c<op2T>, op2T, op1T>>
    using multiply_t = Arithmetic<std::multiplies<>, op1T, op2T, resultT>;

    // division
    template <
        class op1T, class op2T = op1T, class resultT = std::conditional_t<tile_c<op2T>, op2T, op1T>>
    using divide_t = Arithmetic<std::divides<>, op1T, op2T, resultT>;

    // functions of a complex value
    template <class signalT, class amplitudeT>
    using amplitude_t = Amplitude<signalT, amplitudeT>;

    template <class signalT, class phaseT>
    using phase_t = Phase<signalT, phaseT>;
} // namespace pyre::flow::factories::operators


// end of file
