// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// the package
#include <pyre/journal.h>


// exercise throwing and catching {firewall_error}
int main() {

    // set up a net
    try {
        // raise the exception
        throw pyre::journal::firewall_error("firewall error example");
    }
    // catch the firewall
    catch (const pyre::journal::firewall_error & error) {
        // extract the reason
        std::string what = error.what();
        // if it doesn't match what we supplied
        if (what != "firewall error example") {
            // indicate failure
            return 1;
        }
    }
    catch (...) {
        // something else happened; indicate failure
        return 1;
    }

    // all good
    return 0;
}


// end of file
