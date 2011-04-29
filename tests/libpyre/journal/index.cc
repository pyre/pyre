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
typedef pyre::journal::Index<bool> index_t;

// main program
int main() {

    // instantiate an index
    index_t index;

    // request a key that is not there
    bool & state = index.lookup("debug", "test");
    // verify that this is off by default
    assert(state == false);
    // turn it on
    state = true;

    // ask for it again, this time read only
    bool again = index.lookup("debug", "test");
    // verify that it is now on
    assert(again == true);

    // all done
    return 0;
}

// end of file
