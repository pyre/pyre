// -*- c -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal/debuginfo.h>


// exercise the C bindings
int main() {
    // name a channel
    const char * channel = "tests.journal.debuginfo";
    // activate it
    debuginfo_activate(channel);
    // if the channel is active
    if (debuginfo_active(channel)) {
        // deactivate it
        debuginfo_deactivate(channel);
    }

    // say something
    debuginfo_out(channel, __HERE__, "%s", "hello world");

    // all done
    return 0;
}


// end of file
