// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "../external.h"
#include "../products/forward.h"


// forward declarations
namespace pyre::flow::factories {
    // binary operators
    template <template <typename> class categoryT, class op1T, class op2T, class resultT>
    class Binary;

    // addition; the general case is not implemented
    template <template <typename> class categoryT, class op1T, class op2T, class resultT>
    class Add;
    template <class op1T, class op2T, class resultT>
    class Add<products::Tile, op1T, op2T, resultT>;
    template <class op1T, class op2T, class resultT>
    class Add<products::Variable, op1T, op2T, resultT>;

    // multiplication; the general case is not implemented
    template <template <typename> class categoryT, class op1T, class op2T, class resultT>
    class Multiply;
    template <class op1T, class op2T, class resultT>
    class Multiply<products::Tile, op1T, op2T, resultT>;
    template <class op1T, class op2T, class resultT>
    class Multiply<products::Variable, op1T, op2T, resultT>;
} // namespace pyre::flow::factories


// end of file
