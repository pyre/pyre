// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
// instantiate a functional index
using index_t = pyre::journal::index_t;
// the trash can
using trash_t = pyre::journal::trash_t;


// exercise the cascade feature of the channel state index
int main() {
    // make an index
    index_t index(true, false);

    // lookup a name
    auto & parent = index.lookup("test.index.parent");
    // make sure its activation state is what's expected
    assert(parent.active() == index.active());
    // its fatal state is what's expected
    assert(parent.fatal() == index.fatal());
    // and the device is null
    assert(parent.device() == nullptr);
    // turn it off
    parent.active(false);
    // and make it fatal
    parent.fatal(true);
    // make sure it happened
    assert(parent.active() == false);
    // set the device to a trash can
    parent.device<trash_t>();

    // lookup a name that's lower in the hierarchy
    auto & child = index.lookup("test.index.parent.blah.blah.child");
    // make sure its actual state is what's expected
    assert(child.active() == parent.active());
    // check its fatal state is what's expected
    assert(child.fatal() == parent.fatal());
    // and that it inherited the device
    assert(child.device() == parent.device());

    // all done
    return 0;
}


// end of file
