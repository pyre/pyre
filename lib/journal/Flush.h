// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// flush a channel after injecting a decorator
template <typename decoratorT>
class pyre::journal::Flush {
public:
    using decorator_type = decoratorT;

    // metamethods
public:
    // constructor
    inline Flush(decorator_type decorator);

    // interface
public:
    inline auto decorator() const -> const decorator_type &;

    // data
private:
    decorator_type _decorator;
};


// get the inline definitions
#include "Flush.icc"


// end of file
