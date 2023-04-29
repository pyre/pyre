// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise decorating a message with a code
int
main()
{
    // make a channel
    pyre::journal::info_t channel("tests.journal.info");

    // set the chronicler maximum detail level so the code is rendered
    pyre::journal::chronicler_t::decor(2);
    // activate it
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // inject something into the channel
    channel
        // add the code
        << pyre::journal::code(10)
        // say something
        << "hello world!"
        // and flush
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
