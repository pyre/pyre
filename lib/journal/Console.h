// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once

// a device that prints to {cout}
class pyre::journal::Console : public Stream {
    // types
public:
    // pointers to me
    using pointer_type = std::shared_ptr<Console>;

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
