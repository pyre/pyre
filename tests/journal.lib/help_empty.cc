// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// verify that empty injections in help channels happen correctly
int
main()
{
    // make a help channel
    pyre::journal::help_t channel("tests.journal.help");
    // send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // inject nothing
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
