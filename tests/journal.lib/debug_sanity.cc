// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that the debug diagnostic is off by default, and that we can manipulate its state
int
main()
{
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");

    // check its name
    assert(channel.name() == "tests.journal.debug");
    // by default, detail should be 1
    assert(channel.detail() == 1);
    // by default, dent should be 0
    assert(channel.dent() == 0);
    // by default, it should be inactive
    assert(channel.active() == false);
    // and non-fatal
    assert(channel.fatal() == false);

    // make a debug channel with detail and dent
    const pyre::journal::detail_t detail = 2;
    const pyre::journal::dent_t dent = 1;
    pyre::journal::debug_t channel2("tests.journal.debug2", detail, dent);

    // check its name
    assert(channel2.name() == "tests.journal.debug2");
    // detail should match specified value
    assert(channel2.detail() == detail);
    // dent should match specified value
    assert(channel2.dent() == dent);
    // by default, it should be inactive
    assert(channel2.active() == false);
    // and non-fatal
    assert(channel2.fatal() == false);

    // all done
    return 0;
}


// end of file
