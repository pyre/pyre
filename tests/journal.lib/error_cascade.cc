// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
// chronicler
using chronicler_t = pyre::journal::chronicler_t;
// error
using myerror_t = pyre::journal::error_t;
// the trash can
using trash_t = pyre::journal::trash_t;


// verify the cascade works correctly for errors
int main() {
    // make a channel
    myerror_t parent("test.error.parent");
    // its activation state is what's expected
    assert(parent.active());
    // it is fatal
    assert(parent.fatal());
    // and the device is the global default
    assert(parent.device() == chronicler_t::device());
    // turn it off
    parent.deactivate();
    // make it non-fatal
    parent.fatal(false);
    // and set the device to a trash can
    parent.device<trash_t>();

    // make a channel that's lower in the hierarchy
    myerror_t child("test.error.parent.blah.blah.child");
    // make sure its activation state is what's expected
    assert(child.active() == parent.active());
    // it is also non-fatal
    assert(child.fatal() == parent.fatal());
    // and that it inherited the device
    assert(child.device() == parent.device());

    // all done
    return 0;
}


// end of file
