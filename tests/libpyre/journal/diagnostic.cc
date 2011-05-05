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
#include <vector>
#include <string>
#include <sstream>
#include <iostream>

// access to the low level diagnostic header file
#include <pyre/journal/Diagnostic.h>

class Debug : public pyre::journal::Diagnostic<Debug> {
public:
    bool isActive() const { return true; }
};

typedef pyre::journal::Diagnostic<Debug> diagnostic_t;


// main program
int main() {

    // instantiate
    diagnostic_t d;

    // all done
    return 0;
}

// end of file
