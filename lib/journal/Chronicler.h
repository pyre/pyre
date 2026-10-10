// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// singleton that owns the journal default configuration
class pyre::journal::Chronicler {
    // types
public:
    // me
    using self_type = Chronicler;

    // strings;
    using string_type = string_t;
    // detail level
    using detail_type = detail_t;
    // the margin type
    using margin_type = string_type;
    // global metadata
    using key_type = key_t;
    using value_type = value_t;
    using notes_type = notes_t;

    // device support
    using device_type = std::shared_ptr<Device>;
    // the devices a walk over the installed devices has already examined
    using visited_type = std::set<const Device *>;
    // the per-severity shared state of the channels
    using index_type = Index;
    // the shared state of a channel
    using inventory_type = Inventory;

    // channel names
    using name_type = name_t;
    using nameset_type = nameset_t;

    // command line parsing
    using cmdname_type = cmdname_t;
    using cmdvalue_type = cmdvalue_t;
    using cmd_type = cmd_t;

    // metamethods
public:
    // destructor; i am never instantiated, but the bindings must be able to name it
    ~Chronicler() = default;

    // interface
public:
    // the initializer that parses the program command line
    static void init(int argc, char * argv[]);

    // suppress all output
    static void quiet();

    // decoration level filter
    static inline auto decor() -> detail_type;
    static inline auto decor(detail_type) -> detail_type;
    // detail level filter
    static inline auto detail() -> detail_type;
    static inline auto detail(detail_type) -> detail_type;

    // print margin control
    static inline auto margin() -> margin_type;
    static inline auto margin(margin_type) -> margin_type;

    // metadata
    static inline auto notes() -> notes_type &;
    // device support
    static inline auto device() -> device_type;
    static inline void device(device_type);

    template <class deviceT, class... Args>
    static inline void device(Args &&... args);
    // detach every foreign device from the journal, wherever it is installed: the default device,
    // the defaults of the severities, the devices of individual channels, and the outputs and
    // mirrors of the devices that forward entries to others; a foreign default device is
    // replaced by a console, and every other foreign device is forgotten, so the channels fall
    // back on the devices above them
    static void detachForeign();

    // convert a string with a comma separated list of names into a set
    static inline auto nameset(string_type) -> nameset_type;

    // implementation details
private:
    // detach the foreign devices from the default of a severity and from each of its channels
    static void sweepIndex(index_type &, visited_type &);
    // detach a foreign device from the shared state of a channel
    static void sweepInventory(inventory_type &, visited_type &);
    // detach the foreign devices among those a device forwards entries to
    static void prune(const device_type &, visited_type &);

    // data members
private:
    static device_type _device;
    static notes_type _notes;
    static detail_type _decor;
    static detail_type _detail;
    static string_type _margin;

    // disallow
private:
    Chronicler() = delete;
    Chronicler(const Chronicler &) = delete;
    Chronicler(Chronicler &&) = delete;
    Chronicler & operator=(const Chronicler &) = delete;
    Chronicler & operator=(Chronicler &&) = delete;
};


// get the inline definitions
#include "Chronicler.icc"


// end of file
