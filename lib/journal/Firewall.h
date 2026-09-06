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
// the proxy that binds a channel to its shared state
#include "InventoryProxy.h"
// my parts
#include "exceptions.h"
#include "Chronicler.h"


// developer facing channel; usually gets turned off in release mode
template <template <typename> typename proxyT>
class pyre::journal::Firewall : public Channel<Firewall<proxyT>, proxyT> {
    // types
public:
    // me
    using self_type = Firewall<proxyT>;
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
    using exception_type = firewall_error;

    // metamethods
public:
    inline explicit Firewall(const name_type &, detail_type = 1, dent_type = 0);

    // implementation details
public:
    // record the message to a device
    inline void record();
    // raise the correct exception when fatal
    inline void die();

    // implementation details
public:
    // initialize the channel index
    static inline auto initializeIndex() -> index_type;

    // disallow
private:
    Firewall(const Firewall &) = delete;
    Firewall(const Firewall &&) = delete;
    const Firewall & operator=(const Firewall &) = delete;
    const Firewall & operator=(const Firewall &&) = delete;
};


// get the inline definitions
#include "Firewall.icc"


// the channel index is a static data member of a class template, so every translation unit
// that touches the channel would otherwise carry its own definition; a linker that does not
// unify such definitions across shared objects then splits the channel state between the
// library and every extension module that uses it, and a channel deactivated in one is still
// active in the other; so the index is declared here as an explicit specialization, which
// makes it an ordinary variable with one definition, in the library
template <>
pyre::journal::Index pyre::journal::Channel<
    pyre::journal::Firewall<pyre::journal::InventoryProxy>, pyre::journal::InventoryProxy>::_index;


// end of file
