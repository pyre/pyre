// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Error_h)
#define pyre_journal_Error_h


// user facing channel; meant for error messages, i.e. conditions from which the application
// cannot recover
template <template <typename> typename proxyT>
class pyre::journal::Error : public Channel<Error<proxyT>, proxyT>
{
    // types
public:
    // my base
    using channel_type = Channel<Error, InventoryProxy>;
    // my parts
    using name_type = typename channel_type::name_type;
    using detail_type = typename channel_type::detail_type;
    using index_type = typename channel_type::index_type;
    using entry_type = typename channel_type::entry_type;
    // my error indicator
    using exception_type = application_error;

    // metamethods
public:
    inline explicit Error(const name_type & name, detail_type = 1);

    // implementation details
public:
    // record the message in the journal
    inline void record();
    // raise the correct exception when fatal
    inline void die();

    // implementation details
public:
    // initialize the channel index
    static inline auto initializeIndex() -> index_type;

    // disallow
private:
    Error(const Error &) = delete;
    Error(const Error &&) = delete;
    const Error & operator= (const Error &) = delete;
    const Error & operator= (const Error &&) = delete;
};


// get the inline definitions
#define pyre_journal_Error_icc
#include "Error.icc"
#undef pyre_journal_Error_icc


#endif

// end of file
