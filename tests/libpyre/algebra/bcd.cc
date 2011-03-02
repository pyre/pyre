// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

// build system
#include <portinfo>

// system includes
#include <assert.h>

// dependencies
#include <pyre/algebra/BCD.h>

// make short alias for the BCD type we are testing
typedef pyre::algebra::BCD<10, unsigned int> bcd;


// main program
int main(int argc, char* argv[]) {

    // default constructor
    bcd zero;
    assert(zero == 0);

    // constructor with explicit arguments
    bcd one(1,0);
    assert(one == 1);

    // copy constructor
    bcd copy(one);
    assert(copy == one);

    // operator =
    bcd another = one;
    assert(copy == one);

    // operator +
    assert(zero + zero == 0.0);
    assert(one + zero == 1.0);
    assert(zero + one == 1.0);
    assert(one + one == 2.0);

    // exercise the overflow logic
    bcd almost(0,9);
    assert(almost + almost == 1.8);
    
    // all done
    return 0;
}


// end of file
