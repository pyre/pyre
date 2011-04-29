// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


// for the build system
#include <portinfo>

// packages
#include <assert.h>
// access to the packages used by Index
#include <map>
#include <string>
#include <cstdlib>

// access to the low level index header file
#include <pyre/journal/Index.h>

// convenience
typedef pyre::journal::Index index_t;

// main program
int main() {

    // instantiate an index
    index_t index;

    // request a couple of keys that are known to be present, as a result of the environment
    // variable setting in the makefile invocation
    index_t::state_t test1 = index.lookup("debug", "pyre.journal.test1");
    index_t::state_t test2 = index.lookup("debug", "pyre.journal.test2");
    // verify that they are activated
    assert(test1 == true);
    assert(test2 == true);

    // all done
    return 0;
}

// end of file
