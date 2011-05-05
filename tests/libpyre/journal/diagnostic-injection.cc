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
#include <map>
#include <string>
#include <iostream>
#include <sstream>

// access to the low level diagnostic header file
#include <pyre/journal/Diagnostic.h>
#include <pyre/journal/macros.h>
#include <pyre/journal/manipulators.h>


// a simple channel class
class Debug : public pyre::journal::Diagnostic<Debug> {
public:
    bool isActive() const { return true; }
};


// main program
int main() {

    // instantiate
    Debug d;
   
    // inject
    d 
        << pyre::journal::at(__HERE__)
        << pyre::journal::set("key", "value")
        << pyre::journal::newline
        << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
