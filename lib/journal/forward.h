// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved

// code guard
#if !defined(pyre_journal_forward_h)
#define pyre_journal_forward_h


// grab the locator macros
#include "macros.h"


// forward declarations of all user facing entities
namespace pyre::journal {
    // abstractions
    class Device;
    class Renderer;

    // the global state
    class Chronicler;

    // message
    class Entry;

    // the channel stream manipulators; some are actual classes, others are functions that take
    // and return a channel
    // verbosity level
    class Verbosity;
    // location information
    class Locator;
    // metadata manipulation
    class Note;
    // flushing with a decorator
    template <typename decoratorT> class Flush;

    // renderers
    class Memo;
    class Alert;

    // devices
    class Trash;
    class File;
    class Stream;
    class Console;
    class ErrorConsole;

    // the null channel; used when developer facing channels are turned off at compile time
    class Null;
    // end of transaction
    inline constexpr auto endl(const Null &) -> const Null &;
    // mark the end of a line of output
    inline constexpr auto newline(const Null &) -> const Null &;
    // injection operators
    // verbosity level
    inline constexpr auto
    operator<< (const Null &, const Verbosity &) -> const Null &;
    // location info
    inline constexpr auto
    operator<< (const Null &, const Locator &) -> const Null &;
    // metadata
    inline constexpr auto
    operator<< (const Null &, const Note &) -> const Null &;
    // injection of a manipulator function
    inline constexpr auto
    operator<< (const Null &, const Null & (*)(const Null &)) -> const Null &;
    // injection of everything else
    template <typename itemT>
    inline constexpr auto
    operator<< (const Null &, const itemT &) -> const Null &;

    // support for sharing state among channels of the same severity+name
    // the shared state parts
    class Inventory;
    // shared access to the shared state
    template <class clientT> class InventoryProxy;
    // storage/retrieval of shared state based on the channel name
    class Index;

    // channel parts
    template <class severityT, template <typename> class proxyT = InventoryProxy> class Channel;

    // channels
    // user facing facing
    // info
    template <template <typename> typename proxyT>
    class Informational;
    // warning
    template <template <typename> typename proxyT>
    class Warning;
    // error
    template <template <typename> typename proxyT>
    class Error;

    // developer facing
    // debug
    template <template <typename> typename proxyT>
    class Debug;
    // firewalls
    template <template <typename> typename proxyT>
    class Firewall;

    // end of transaction
    template <typename severityT, template <class> typename proxyT>
    inline auto
    endl(Channel<severityT, proxyT> &) -> Channel<severityT, proxyT> &;

    // flushing with a decorator
    template <typename decoratorT>
    inline auto endl(decoratorT) -> Flush<decoratorT>;

    // flushing with the special locator signature
    inline auto endl(__HERE_DECL__) -> Flush<Locator>;

    // end of a line of output
    template <typename severityT, template <class> typename proxyT>
    inline auto
    newline(Channel<severityT, proxyT> &) -> Channel<severityT, proxyT> &;

    // injection operators
    // verbosity info
    template <typename severityT, template <class> typename proxyT>
    inline auto
    operator<< (Channel<severityT, proxyT> &, const Verbosity &) -> Channel<severityT, proxyT> &;

    // location info
    template <typename severityT, template <class> typename proxyT>
    inline auto
    operator<< (Channel<severityT, proxyT> &, const Locator &) -> Channel<severityT, proxyT> &;

    // metadata
    template <typename severityT, template <class> typename proxyT>
    inline auto
    operator<< (Channel<severityT, proxyT> &, const Note &) -> Channel<severityT, proxyT> &;

    // flush with a decorator
    template <typename severityT, template <class> typename proxyT, typename decoratorT>
    inline auto
    operator<< (Channel<severityT, proxyT> & channel, const Flush<decoratorT> & flush)
        -> Channel<severityT, proxyT> &;

    // injection of manipulator functions
    template <typename severityT, template <class> typename proxyT>
    inline auto
    operator<< (Channel<severityT, proxyT> &,
                Channel<severityT, proxyT> & (*)(Channel<severityT, proxyT> &))
        -> Channel<severityT, proxyT> &;

    // injection of everything else
    template <typename itemT, typename severityT, template <class> typename proxyT>
    inline auto
    operator<< (Channel<severityT, proxyT> &, const itemT &) -> Channel<severityT, proxyT> &;

    // the exceptions
    class application_error;
    class debug_error;
    class firewall_error;

    // terminal support
    class ASCII;
    class CSI;
    class ANSI;
}


# endif

// end of file
