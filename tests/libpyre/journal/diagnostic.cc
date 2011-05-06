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
    // types
public:
    typedef std::string string_t;
    // meta methods
public:
    Debug(string_t name) : Diagnostic<Debug>("debug", name) {}
};


// main program
int main() {

    // instantiate
    Debug d("pyre.journal.test");

    // all done
    return 0;
}

// end of file
