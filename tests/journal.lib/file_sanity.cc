// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias the type
using file_t = pyre::journal::file_t;


// exercise the stream device
int main() {
    // the filename
    auto filename = file_t::path_type("file_sanity.out");

    // instantiate
    file_t file(filename);
    // check its name
    assert (file.name() == "file");
    // and its path
    assert (file.path() == filename);

    // all done
    return 0;
}


// end of file
