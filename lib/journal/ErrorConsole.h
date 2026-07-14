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


// a device that prints to {cerr}
class pyre::journal::ErrorConsole : public Stream {
    // types
public:
    // me
    using self_type = ErrorConsole;
    // pointers to me
    using pointer_type = std::shared_ptr<self_type>;
    // my superclass
    using super_type = Stream;

    // metamethods
public:
    // constructor
    ErrorConsole();
    // destructor
    virtual ~ErrorConsole();

    // interface
public:
    inline bool tty() const;

    // data
private:
    bool _tty;

    // disallow
private:
    ErrorConsole(const ErrorConsole &) = delete;
    ErrorConsole(const ErrorConsole &&) = delete;
    const ErrorConsole & operator=(const ErrorConsole &) = delete;
    const ErrorConsole & operator=(const ErrorConsole &&) = delete;
};


// get the inline definitions
#include "ErrorConsole.icc"


// end of file
