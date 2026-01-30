// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias
using myhelp_t = pyre::journal::help_t;


// verify the basic channel state
int
main()
{
    // make an help channel
    myhelp_t channel("tests.journal.help");

    // check its name
    assert(channel.name() == "tests.journal.help");
    // by default, detail should be 1
    assert(channel.detail() == 1);
    // by default, dent should be 0
    assert(channel.dent() == 0);
    // by default, it should be active
    assert(channel);
    // and non-fatal
    assert(channel.fatal() == false);

    // make an help channel with detail and dent
    const pyre::journal::detail_t detail = 2;
    const pyre::journal::dent_t dent = 1;
    pyre::journal::help_t channel2("tests.journal.help2", detail, dent);

    // check its name
    assert(channel2.name() == "tests.journal.help2");
    // detail should match specified value
    assert(channel2.detail() == detail);
    // dent should match specified value
    assert(channel2.dent() == dent);
    // by default, it should be active
    assert(channel2);
    // and non-fatal
    assert(channel2.fatal() == false);

    // all done
    return 0;
}


// end of file
