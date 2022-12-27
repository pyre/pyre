// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Warning_h)
#define pyre_journal_Warning_h


// user facing channel ; meant for warning messages, i.e. when the applications detects
// something wrong but it can work around the problem
template <template <typename> typename proxyT>
class pyre::journal::Warning : public Channel<Warning<proxyT>, proxyT>
{
    // types
public:
    // my base
    using channel_type = Channel<Warning, InventoryProxy>;
    // my parts
    using name_type = typename channel_type::name_type;
    using detail_type = typename channel_type::detail_type;
    using index_type = typename channel_type::index_type;
    using entry_type = typename channel_type::entry_type;
    // my exception
    using exception_type = application_error;

    // metamethods
public:
    inline explicit Warning(const name_type & name, detail_type = 1);

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
    Warning(const Warning &) = delete;
    Warning(const Warning &&) = delete;
    const Warning & operator= (const Warning &) = delete;
    const Warning & operator= (const Warning &&) = delete;
};


// get the inline definitions
#define pyre_journal_Warning_icc
#include "Warning.icc"
#undef pyre_journal_Warning_icc


#endif

// end of file
