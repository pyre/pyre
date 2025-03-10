// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// alias
using chronicler_t = pyre::journal::chronicler_t;


// verify that the decor level set in the environment matches what the test harness gave me
// on the command line
int
main(int argc, char * argv[])
{
    // make sure we get one command line argument
    assert(argc == 2);
    // get the decor
    auto decor = chronicler_t::decor();
    // interpret the command line argument as the intended level
    pyre::journal::detail_t expected = std::atoi(argv[1]);
    // verify they match
    assert(decor == expected);

    // all done
    return 0;
}


// end of file
