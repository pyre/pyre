// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "../../forward.h"
#include "../../products/forward.h"
// the rules of arithmetic
#include "concepts.h"


// forward declarations
namespace pyre::flow::factories::operators {
    // binary operators
    template <class op1T, class op2T, class resultT>
    class Binary;

    // the arithmetic: an operation, such as {std::plus<>}, that combines two operands, each a
    // scalar or a tile, as long as the math says the combination makes sense
    template <class operationT, class op1T, class op2T, class resultT>
        requires arithmetic_c<operationT, op1T, op2T, resultT>
    class Arithmetic;

    // functions of a complex value
    template <class signalT, class amplitudeT>
    class Amplitude;
    template <class signalT, class phaseT>
    class Phase;
} // namespace pyre::flow::factories::operators


// end of file
