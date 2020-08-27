// -*- c++ -*-
//
// the pyre authors
// (c) 1998-2020 all rights reserved

#include <pyre/journal.h>
#include <cassert>

using pyre::journal::tee_t;

// exercise the tee device
int main() {

    tee_t tee{"file_a.log",
              "file_b.log"};

    assert(tee.outputs().size() == 3);
}

// end of file
