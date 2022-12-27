// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias the type
using debug_t = pyre::journal::debug_t;
using file_t = pyre::journal::file_t;


// exercise the file device
int main() {
    // the filename
    auto filename = file_t::path_type("file_example.out");

    // make a channel
    debug_t channel("test.journal.file");
    // set its device
    channel.device<file_t>(filename);
    // activate
    channel.activate();

    // inject something
    channel
        << pyre::journal::at(__HERE__)
        << "hello world!"
        << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
