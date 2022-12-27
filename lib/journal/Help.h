// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Help_h)
#define pyre_journal_Help_h


// user facing channel; meant for informational messages, such as progress reports
template <template <typename> typename proxyT>
class pyre::journal::Help : public Channel<Help<proxyT>, proxyT> {
    // types
public:
    // my base
    using channel_type = Channel<Help<proxyT>, proxyT>;
    // my parts
    using name_type = typename channel_type::name_type;
    using detail_type = typename channel_type::detail_type;
    using index_type = typename channel_type::index_type;
    using entry_type = typename channel_type::entry_type;
    // my exception
    using exception_type = application_error;

    // metamethods
public:
    inline explicit Help(const name_type & name, detail_type = 1);

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
    Help(const Help &) = delete;
    Help(const Help &&) = delete;
    const Help & operator=(const Help &) = delete;
    const Help & operator=(const Help &&) = delete;
};


// get the inline definitions
#define pyre_journal_Help_icc
#include "Help.icc"
#undef pyre_journal_Help_icc


#endif

// end of file
