// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// build as the library itself
// clear the settings of the build
#undef PYRE_CORE
#undef DEBUG
#undef NDEBUG
#undef JOURNAL_DEBUG
// declare that this is the library
#define PYRE_CORE

// get the journal
#include <pyre/journal.h>
// support
#include <type_traits>


// the guard records that the developer channels are live
static_assert(JOURNAL_DEBUG == 1);
// and the firewall channel is live
static_assert(!std::is_same_v<pyre::journal::firewall_t, pyre::journal::null_t>);
// as is the debug channel
static_assert(!std::is_same_v<pyre::journal::debug_t, pyre::journal::null_t>);


// the code behind the guard runs exactly when the developer channels are live
int
main()
{
    // count the exceptions raised by the guarded code
    auto raised = 0;

    // when the developer channels are live
#if JOURNAL_DEBUG
    // make a channel
    pyre::journal::firewall_t channel("tests.journal.guard");
    // send its output to the trash
    channel.device<pyre::journal::trash_t>();
    // carefully
    try {
        // raise what the channel hands back
        throw channel << "the guarded firewall" << pyre::journal::endl;
    }
    // if it is the exception that states the condition
    catch (const pyre::journal::firewall_error &) {
        // count it
        ++raised;
    }
#endif

    // the guarded code raised once if the channels are live, and never if they are null
    return raised == JOURNAL_DEBUG ? 0 : 1;
}


// end of file
