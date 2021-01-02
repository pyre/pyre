// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias
using chronicler_t = pyre::journal::chronicler_t;


// verify that the verbosity level set in the environment matches what the test harness gave me
// on the command line
int main(int argc, char *argv[]) {
    // make sure we get one command line argument
    assert (argc == 2);
    // get the verbosity
    auto verbosity = chronicler_t::verbosity();
    // interpret the command line argument as the intended level
    pyre::journal::verbosity_t expected = std::atoi(argv[1]);
    // verify they match
    assert (verbosity == expected);

    // all done
    return 0;
}


// end of file
