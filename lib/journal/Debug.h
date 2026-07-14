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
#include "Channel.h"
// my parts
#include "exceptions.h"
#include "Chronicler.h"


// developer facing channel; usually gets turned off in release mode
template <template <typename> typename proxyT>
class pyre::journal::Debug : public Channel<Debug<proxyT>, proxyT> {
    // types
public:
    // me
    using self_type = Debug<proxyT>;
    // my superclass
    using super_type = Channel<self_type, proxyT>;

    // my channel
    using channel_type = super_type;
    // my parts
    using name_type = typename channel_type::name_type;
    using detail_type = typename channel_type::detail_type;
    using dent_type = typename channel_type::dent_type;
    using index_type = typename channel_type::index_type;
    using entry_type = typename channel_type::entry_type;
    // my exception
    using exception_type = debug_error;

    // metamethods
public:
    inline Debug(const name_type &, detail_type = 1, dent_type = 0);

    // implementation details; don't access directly
public:
    // record the message in the journal
    inline void record();
    // raise an exception when fatal
    inline void die();

    // static methods
public:
    // initialize the channel index
    static inline auto initializeIndex() -> index_type;

    // disallow
private:
    Debug(const Debug &) = delete;
    Debug(const Debug &&) = delete;
    const Debug & operator=(const Debug &) = delete;
    const Debug & operator=(const Debug &&) = delete;
};


// get the inline definitions
#include "Debug.icc"


// end of file
