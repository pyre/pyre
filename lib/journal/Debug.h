// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Debug_h)
#define pyre_journal_Debug_h


// developer facing channel; usually gets turned off in release mode
template <template <typename> typename proxyT>
class pyre::journal::Debug : public Channel<Debug<proxyT>, proxyT>
{
    // types
public:
    // my base
    using channel_type = Channel<Debug<proxyT>, proxyT>;
    // my parts
    using name_type = typename channel_type::name_type;
    using detail_type = typename channel_type::detail_type;
    using index_type = typename channel_type::index_type;
    using entry_type = typename channel_type::entry_type;
    // my exception
    using exception_type = debug_error;

    // metamethods
public:
    inline Debug(const name_type &, detail_type = 1);

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
    const Debug & operator= (const Debug &) = delete;
    const Debug & operator= (const Debug &&) = delete;
};


// get the inline definitions
#define pyre_journal_Debug_icc
#include "Debug.icc"
#undef pyre_journal_Debug_icc


#endif

// end of file
