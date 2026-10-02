// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// end user facing api
namespace pyre::journal {
    // the initializer of the global settings
    inline void init(int argc, char * argv[]);
    // registration of the application name; {value_t} is normally an {std::string}
    inline void application(const value_t & name);
    // manipulate the detail threshold
    inline void setDetail(int);
    // turn all channel output off
    inline void quiet();
    // send all channel output to a log file
    inline void logfile(const path_t &, filemode_t mode = std::ios_base::out);

    // channels
    using info_t = Informational<InventoryProxy>;
    using warning_t = Warning<InventoryProxy>;
    using error_t = Error<InventoryProxy>;
    using help_t = Help<InventoryProxy>;

    // the keeper of the global settings
    using chronicler_t = Chronicler;

    // devices
    using trash_t = Trash;
    using file_t = File;
    using stream_t = Stream;
    using cout_t = Console;
    using cerr_t = ErrorConsole;
    using courier_t = Courier;
    using splitter_t = Splitter;
    using tee_t = Tee;

    // manipulators
    using at = Locator;
    using here = Locator;
    using note = Note;
    using detail = Detail;
    // the backwards compatible api; deprecated, and will be removed in 2.0
    using verbosity = Detail;
} // namespace pyre::journal


// the developer channels, {debug_t} and {firewall_t}, are live or null depending on the build:
// {JOURNAL_DEBUG}, when set to 0 or 1, decides; otherwise {NDEBUG} turns them off and {DEBUG}
// turns them on, with {NDEBUG} winning when both are present, and they are off when neither is;
// the library itself is always built with them on. on the way out, {JOURNAL_DEBUG} is always
// defined, as 1 when the channels are live and 0 when they are null, so clients can guard code
// that only compiles against the live channels, such as {throw firewall << ... << endl;}, with
// {#if JOURNAL_DEBUG}
// if we are building the library
#if defined(PYRE_CORE)
// the developer channels are live, so a request to turn them off cannot be honored
#if defined(JOURNAL_DEBUG) && !JOURNAL_DEBUG
#error "the journal developer channels are always live in the library; JOURNAL_DEBUG must not be 0"
#endif
// if there is no setting
#if !defined(JOURNAL_DEBUG)
// record that the developer channels are live
#define JOURNAL_DEBUG 1
#endif
// if the user has decided explicitly
#elif defined(JOURNAL_DEBUG)
// there is nothing to record; the setting picks the channels below
// if the user has suppressed debugging support
#elif defined(NDEBUG)
// record that the developer channels are null
#define JOURNAL_DEBUG 0
// if the user has requested debugging support
#elif defined(DEBUG)
// record that the developer channels are live
#define JOURNAL_DEBUG 1
// otherwise, this is a production build
#else
// record that the developer channels are null
#define JOURNAL_DEBUG 0
#endif


// the developer facing api
namespace pyre::journal {
    // null diagnostic: always available
    using null_t = Null;

    // if the developer channels are live
#if JOURNAL_DEBUG
    // enable them
    using debug_t = Debug<InventoryProxy>;
    using firewall_t = Firewall<InventoryProxy>;

    // otherwise
#else
    // disable them
    using debug_t = null_t;
    using firewall_t = null_t;
#endif
} // namespace pyre::journal


// low level api; chances are good you shouldn't access these directly
namespace pyre::journal {
    // message entry
    using entry_t = Entry;

    // shared channel state
    using inventory_t = Inventory;

    template <class clientT>
    using inventory_proxy_t = InventoryProxy<clientT>;

    template <class severityT, template <typename> class proxyT = inventory_proxy_t>
    using channel_t = Channel<severityT, proxyT>;

    using index_t = Index;

    // renderers
    using renderer_t = Renderer;
    using renderer_ptr = std::shared_ptr<renderer_t>;
    using alert_t = Alert;
    using bland_t = Bland;
    using memo_t = Memo;

    // devices
    using device_t = Device;
    using device_ptr = std::shared_ptr<Device>;

    // aliases for the manipulators
    using code_t = Code;
    using color_t = Color;
    using indenter_t = Dent;
    using locator_t = Locator;
    using note_t = Note;

    // terminal support
    using ascii_t = ASCII;
    using csi_t = CSI;
    using ansi_t = ANSI;
} // namespace pyre::journal


// end of file
