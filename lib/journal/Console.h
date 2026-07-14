// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once


// my dependencies
#include "forward.h"
// my superclass
#include "Stream.h"


// a device that prints to {cout}
class pyre::journal::Console : public Stream {
    // types
public:
    // me
    using self_type = Console;
    // pointers to me
    using pointer_type = std::shared_ptr<Console>;
    // my superclass
    using super_type = Stream;

    // metamethods
public:
    // constructor
    Console();
    // destructor
    virtual ~Console();

    // interface
public:
    inline bool tty() const;

    // data
private:
    bool _tty;

    // disallow
private:
    Console(const Console &) = delete;
    Console(const Console &&) = delete;
    const Console & operator=(const Console &) = delete;
    const Console & operator=(const Console &&) = delete;
};


// get the inline definitions
#include "Console.icc"


// end of file
