// -*- c -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support for {bool}
#include <stdbool.h>
// get the journal
#include <pyre/journal/firewalls.h>


// exercise the C bindings
int main() {
    // name a channel
    const char * channel = "tests.journal.debuginfo";

    // check a true statement
    firewall_check(channel, true, __HERE__, "something is %s", "wrong");

    // all done
    return 0;
}


// end of file
