// -*- c++ -*-
//
// the pyre authors
// (c) 1998-2020 all rights reserved

#include <pyre/journal.h>
#include <cassert>

using pyre::journal::splitter_t;

int main() {

    // create empty splitter
    {
        splitter_t splitter{};
        assert(splitter.outputs().size() == 0);
    }

    // check that nonce splitter names are unique
    {
        splitter_t a{};
        splitter_t b{};
        assert(a.name() != b.name());
    }
}

// end of file
