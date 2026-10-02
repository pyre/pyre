// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// information about the location of the channel invocation
class pyre::journal::Locator {
    // types
public:
    // me
    using self_type = Locator;
    // the data held by {Locator} are used to create message notes
    using value_type = value_t;

    // metamethods
public:
    // constructor
#if defined(__cpp_lib_source_location)
    // very modern version: the compiler does the work
    inline Locator(const std::source_location = std::source_location::current());
#else
    inline Locator();
#endif
    // modern version; preferred when instantiating explicitly
    inline Locator(const value_type &, const value_type &, const value_type &);
    // legacy version; used by the {__HERE__} locator factories, and deprecated for c++ clients,
    // which get the location from the compiler by using the default constructor instead
    [[deprecated(
        "use pyre::journal::at(), which records the location automatically; "
        "the {__HERE__} form will be removed in pyre 1.15")]]
    inline explicit Locator(const char *, int = 0, const char * = "");

    // interface
public:
    // accessors
    inline auto file() const -> const value_type &;
    inline auto line() const -> const value_type &;
    inline auto func() const -> const value_type &;

    // data
private:
    const value_type _file;
    const value_type _line;
    const value_type _func;
};


// get the inline definitions
#include "Locator.icc"


// end of file
