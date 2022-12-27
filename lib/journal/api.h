// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_api_h)
#define pyre_journal_api_h


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

    // manipulators
    using at = Locator;
    using note = Note;
    using detail = Detail;
    // the backwards compatible api; deprecated, and will be removed in 2.0
    using verbosity = Detail;
} // namespace pyre::journal


// the developer facing api
namespace pyre::journal {
    // null diagnostic: always available
    using null_t = Null;

    // if we are building the library
#if defined(PYRE_CORE)
    // enable the developer channels
    using debug_t = Debug<InventoryProxy>;
    using firewall_t = Firewall<InventoryProxy>;

    // if the user has suppressed debugging support explicitly
#elif defined(NDEBUG)
    // disable the developer channels
    using debug_t = null_t;
    using firewall_t = null_t;

    // if the user has requested debugging support explicitly
#elif defined(DEBUG) || defined(JOURNAL_DEBUG)
    // enable the developer channels
    using debug_t = Debug<InventoryProxy>;
    using firewall_t = Firewall<InventoryProxy>;

    // otherwise, this is a production build
#else
    // disable the developer channels
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


#endif

// end of file
