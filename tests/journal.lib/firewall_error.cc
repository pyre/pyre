// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// the package
#include <pyre/journal.h>


// type alias
using firewall_error = pyre::journal::firewall_error;


// exercise throwing and catching {firewall_error}
int main() {

    // make a headline
    firewall_error::headline_type headline = "firewall error example";
    // an empty message body
    firewall_error::page_type page;
    // and empty notes
    firewall_error::notes_type notes;

    // set up a net
    try {
        // raise the exception
        throw firewall_error(headline, page, notes);
    }
    // catch the firewall
    catch (const pyre::journal::firewall_error & error) {
        // extract the reason
        std::string what = error.what();
        // if it doesn't match what we supplied
        if (what != headline) {
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
