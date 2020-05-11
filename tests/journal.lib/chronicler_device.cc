// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// aliases
using trash_t = pyre::journal::trash_t;
using chronicler_t = pyre::journal::chronicler_t;


// exercise getting/setting the global default device
int main() {
    // get the default device
    auto builtin = chronicler_t::device();

    // make a new device
    auto custom = std::make_shared<trash_t>();
    // install it
    auto old = chronicler_t::device(custom);

    // check that the current device is the one we just installed
    assert (chronicler_t::device().get() == custom.get());
    // and that the device returned during installation is the {builtin} one
    assert (old.get() == builtin.get());

    // all done
    return 0;
}


// end of file
