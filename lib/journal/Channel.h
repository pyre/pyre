// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved

// code guard
#if !defined(pyre_journal_Channel_h)
#define pyre_journal_Channel_h


// the base journal channel
template <typename severityT, template <class> typename proxyT>
class pyre::journal::Channel : public proxyT<severityT>
{
    // types
public:
    // my severity
    using severity_type = severityT;
    using severity_reference = severity_type &;

    // my verbosity
    using verbosity_type = verbosity_t;

    // access to my shared state
    using proxy_type = proxyT<severityT>;
    using inventory_type = typename proxy_type::inventory_type;
    using inventory_reference = typename proxy_type::inventory_reference;
    using device_type = typename inventory_type::device_type;

    // my name
    using name_type = Index::name_type;
    // the map from channel names to inventories
    using index_type = Index;
    using index_reference = index_type &;
    // the current message
    using entry_type = entry_t;
    using entry_reference = entry_type &;
    using entry_const_reference = const entry_type &;

    // pathnames
    using path_type = path_t;

    // miscellaneous
    using string_type = string_t;
    using nameset_type = nameset_t;

    // metamethods
public:
    inline Channel(const name_type &, verbosity_type = 1);

    // accessors
public:
    inline auto name() const -> const name_type &;
    inline auto verbosity() const -> verbosity_type;
    inline auto entry() const -> entry_const_reference;

    // mutators
public:
    // verbosity
    inline auto verbosity(verbosity_type) -> severity_reference;
    // read/write access to my current journal entry
    inline auto entry() -> entry_reference;

    // injection support; not normally accessed directly, there are manipulators for this
public:
    // end of a line of message
    inline auto line() -> severity_reference;
    // end of a message
    inline auto log() -> severity_reference;
    // commit the current message to the journal
    inline auto commit() -> severity_reference;

    // static interface
public:
    // access to the severity wide index with the default settings and the names of the channels
    inline static auto index() -> index_reference;
    // index initializer
    inline static auto initializeIndex() -> index_type;
    // bulk channel activation
    static inline void activateChannels(const nameset_type &);

    // send all output to the trash
    static inline void quiet();
    // and all output to a file with the given filename
    static inline void logfile(const path_t &);

    // implementation details: data
private:
    name_type _name;
    verbosity_type _verbosity;
    entry_type _entry;

    // implementation details: static data
private:
    static inline index_type _index = severity_type::initializeIndex();
};


// get the inline definitions
#define pyre_journal_Channel_icc
#include "Channel.icc"
#undef pyre_journal_Channel_icc


#endif

// end of file
