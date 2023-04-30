// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

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
    // codes
    class Code;
    // color
    class Color;
    // level of detail
    class Detail;
    // indentation
    class Dent;
    // location information
    class Locator;
    // metadata manipulation
    class Note;
    // flushing with a decorator
    template <typename decoratorT>
    class Flush;

    // renderers
    class Alert;
    class Bland;
    class Memo;

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
    // color
    inline constexpr auto operator<<(const Null &, const Color &) -> const Null &;
    // indentation level
    inline constexpr auto operator<<(const Null &, const Dent &) -> const Null &;
    // level of detail
    inline constexpr auto operator<<(const Null &, const Detail &) -> const Null &;
    // location info
    inline constexpr auto operator<<(const Null &, const Locator &) -> const Null &;
    // metadata
    inline constexpr auto operator<<(const Null &, const Note &) -> const Null &;
    // injection of a manipulator function
    inline constexpr auto operator<<(const Null &, const Null & (*) (const Null &) )
        -> const Null &;
    // injection of everything else
    template <typename itemT>
    inline constexpr auto operator<<(const Null &, const itemT &) -> const Null &;

    // support for sharing state among channels of the same severity+name
    // the shared state parts
    class Inventory;
    // shared access to the shared state
    template <class clientT>
    class InventoryProxy;
    // storage/retrieval of shared state based on the channel name
    class Index;

    // channel parts
    template <class severityT, template <typename> class proxyT = InventoryProxy>
    class Channel;

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

    // the help channel
    template <template <typename> typename proxyT>
    class Help;

    // developer facing
    // debug
    template <template <typename> typename proxyT>
    class Debug;
    // firewalls
    template <template <typename> typename proxyT>
    class Firewall;

    // end of transaction
    template <typename severityT, template <class> typename proxyT>
    inline auto endl(Channel<severityT, proxyT> &) -> Channel<severityT, proxyT> &;

    // flushing with a decorator
    template <typename decoratorT>
    inline auto endl(decoratorT) -> Flush<decoratorT>;

    // flushing with the special locator signature
    inline auto endl(__HERE_DECL__) -> Flush<Locator>;

    // end of a line of output
    template <typename severityT, template <class> typename proxyT>
    inline auto newline(Channel<severityT, proxyT> &) -> Channel<severityT, proxyT> &;

    // codes, error and otherwise
    inline auto code(string_t) -> Code;
    template <typename codeT>
    inline auto code(codeT) -> Code;

    // color
    // the various color rep factories
    // known color tables
    inline auto ansi(colorname_t) -> Color;
    inline auto x11(colorname_t) -> Color;
    // ansi control sequences
    inline auto csi3(int, bool = false) -> Color;
    inline auto csi8(int, int, int, bool = true) -> Color;
    inline auto csi8_gray(int, bool = true) -> Color;
    inline auto csi24(int, int, int, bool = true) -> Color;

    // indent
    // the stateful manipulator
    inline auto indent(dent_t level) -> Dent;
    // the stateless manipulator
    template <typename severityT, template <class> typename proxyT>
    inline auto indent(Channel<severityT, proxyT> &) -> Channel<severityT, proxyT> &;

    // outdent
    // the stateful manipulator
    inline auto outdent(dent_t level) -> Dent;
    // the stateless manipulator
    template <typename severityT, template <class> typename proxyT>
    inline auto outdent(Channel<severityT, proxyT> &) -> Channel<severityT, proxyT> &;


    // injection operators
    // code
    template <typename severityT, template <class> typename proxyT>
    inline auto operator<<(Channel<severityT, proxyT> &, const Code &)
        -> Channel<severityT, proxyT> &;

    // color
    template <typename severityT, template <class> typename proxyT>
    inline auto operator<<(Channel<severityT, proxyT> &, const Color &)
        -> Channel<severityT, proxyT> &;

    // indentation level
    template <typename severityT, template <class> typename proxyT>
    inline auto operator<<(Channel<severityT, proxyT> &, const Dent &)
        -> Channel<severityT, proxyT> &;

    // detail level
    template <typename severityT, template <class> typename proxyT>
    inline auto operator<<(Channel<severityT, proxyT> &, const Detail &)
        -> Channel<severityT, proxyT> &;

    // location info
    template <typename severityT, template <class> typename proxyT>
    inline auto operator<<(Channel<severityT, proxyT> &, const Locator &)
        -> Channel<severityT, proxyT> &;

    // metadata
    template <typename severityT, template <class> typename proxyT>
    inline auto operator<<(Channel<severityT, proxyT> &, const Note &)
        -> Channel<severityT, proxyT> &;

    // flush with a decorator
    template <typename severityT, template <class> typename proxyT, typename decoratorT>
    inline auto operator<<(Channel<severityT, proxyT> & channel, const Flush<decoratorT> & flush)
        -> Channel<severityT, proxyT> &;

    // injection of manipulator functions
    template <typename severityT, template <class> typename proxyT>
    inline auto operator<<(
        Channel<severityT, proxyT> &,
        Channel<severityT, proxyT> & (*) (Channel<severityT, proxyT> &) )
        -> Channel<severityT, proxyT> &;

    // injection of everything else
    template <typename itemT, typename severityT, template <class> typename proxyT>
    inline auto operator<<(Channel<severityT, proxyT> &, const itemT &)
        -> Channel<severityT, proxyT> &;

    // the exceptions
    class application_error;
    class debug_error;
    class firewall_error;

    // terminal support
    class ASCII;
    class CSI;
    class ANSI;
}    // namespace pyre::journal


#endif

// end of file
