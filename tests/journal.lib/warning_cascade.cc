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
// warning
using mywarning_t = pyre::journal::warning_t;
// the trash can
using trash_t = pyre::journal::trash_t;


// verify the cascade works correctly for warnings
int main() {
    // make a channel
    mywarning_t parent("test.warning.parent");
    // its activation state is what's expected
    assert(parent.active());
    // it's non-fatal
    assert(parent.fatal() == false);
    // and the device is the global default
    assert(parent.device() == chronicler_t::device());
    // turn it off
    parent.deactivate();
    // and set the device to a trash can
    parent.device<trash_t>();

    // make a warning that's lower in the hierarchy
    mywarning_t child("test.warning.parent.blah.blah.child");
    // make sure its activation state is what's expected
    assert(child.active() == parent.active());
    assert(child.fatal() == parent.fatal());
    // and that it inherited the device
    assert(child.device() == parent.device());

    // all done
    return 0;
}


// end of file
