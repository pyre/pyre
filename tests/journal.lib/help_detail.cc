// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// exercise decorating controlling the channel detail level
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);

    // get the global detail cap, i.e. the highest detail level a journal entry can have before
    // it is silenced
    auto cap = pyre::journal::chronicler_t::detail();

    // make a channel
    pyre::journal::help_t channel("tests.journal.help");
    // send entries to the trash
    channel.device<pyre::journal::trash_t>();

    // get the default channel detail level
    auto defcap = channel.detail();

    // show me
    channel
        // the default detail level
        << "global default detail cap: "
        << cap
        // the channel default detail level
        << "channel default detail level: "
        << defcap
        // and flush
        << pyre::journal::endl;

    // verify that, by default, channels are not filtered out
    assert((cap >= channel.detail()));

    // use the stream manipulator to change the detail level of this channel
    channel << pyre::journal::detail(2) << pyre::journal::endl;
    // verify the change tool place and it survived the flushing of the channel, i.e. it is
    // attached to the channel not the journal entry
    assert((channel.detail() == 2));

    // verify that it's not sticky state, i.e. it is tied to the channel instance not the
    // global channel state that is retrievable by the channel name
    pyre::journal::help_t sister("tests.journal.help");
    // check
    assert((sister.detail() == defcap));

    // all done
    return 0;
}


// end of file
