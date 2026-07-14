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


// user facing channel; meant for error messages, i.e. conditions from which the application
// cannot recover
template <template <typename> typename proxyT>
class pyre::journal::Error : public Channel<Error<proxyT>, proxyT> {
    // types
public:
    // me
    using self_type = Error<proxyT>;
    // my superclass
    using super_type = Channel<self_type, InventoryProxy>;

    // my channel
    using channel_type = super_type;
    // my parts
    using name_type = typename channel_type::name_type;
    using detail_type = typename channel_type::detail_type;
    using dent_type = typename channel_type::dent_type;
    using index_type = typename channel_type::index_type;
    using entry_type = typename channel_type::entry_type;
    // my error indicator
    using exception_type = application_error;

    // metamethods
public:
    inline explicit Error(const name_type & name, detail_type = 1, dent_type = 0);

    // implementation details
public:
    // record the message in the journal
    inline void record();
    // raise the correct exception when fatal
    inline void die();

    // implementation details
public:
    // initialize the channel index
    static inline auto initializeIndex() -> index_type;

    // disallow
private:
    Error(const Error &) = delete;
    Error(const Error &&) = delete;
    const Error & operator=(const Error &) = delete;
    const Error & operator=(const Error &&) = delete;
};


// get the inline definitions
#include "Error.icc"


// end of file
