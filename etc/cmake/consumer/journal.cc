// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal, the way a downstream client would
#include <pyre/journal.h>


// verify that {libjournal} is consumable on its own, i.e. that its headers are installed where
// the exported target says they are and that its symbols resolve at load time
int
main()
{
    // make a channel
    auto channel = pyre::journal::info_t("pyre.consumer.journal");
    // mute it, so that a successful run says nothing
    channel.deactivate();
    // and exercise it; this is what pulls a symbol out of the library
    channel << "the installed journal is reachable" << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
