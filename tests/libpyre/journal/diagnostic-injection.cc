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

    Debug & record() {
        std::cout << "    endl" << std::endl;
        return *this;
    }

    Debug & newline() {
        std::cout << "    newline" << std::endl;
        return *this;
    }

    Debug & print(const char * text) {
        std::cout << "    " << text << std::endl;
        return *this;
    }

public:
    ~Debug() {
        std::cout << " -- destroying a diagnostic" << std::endl;
    }

    Debug() :
        pyre::journal::Diagnostic<Debug>::Diagnostic()
    {
        std::cout << " ++ creating a diagnostic" << std::endl;
    }

    Debug(const Debug & other) :
        pyre::journal::Diagnostic<Debug>::Diagnostic(other)
    {
        std::cout << " ** copying a diagnostic" << std::endl;
    }

    Debug &
    operator = (const Debug & other)
    {
        std::cout << " ** assigning a diagnostic" << std::endl;
        // skip assignment to self
        if (&other != this) {
            // otherwise, copy the data
            pyre::journal::Diagnostic<Debug>::operator=(other);
        }
        // and return me
        return *this;
    }


};


typedef pyre::journal::Diagnostic<Debug> diagnostic_t;


// main program
int main() {

    // instantiate
    diagnostic_t d;
   
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
