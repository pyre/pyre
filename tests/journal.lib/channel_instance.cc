// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// channel stub
class severity_t : public pyre::journal::channel_t<severity_t> {
    // metamethods
public:
    inline explicit severity_t(const name_type & name, verbosity_type verbosity = 1) :
        pyre::journal::channel_t<severity_t>(name, verbosity) {}
};


// verify that diagnostics can be instantiated correctly
int main() {
    // make a diagnostic
    severity_t d1("d1");
    // make sure its verbosity is at the default value
    assert (d1.verbosity() == 1);

    // make another diagnostic with a non-default verbosity
    severity_t d2("d3", 3);
    // make sure its verbosity is at the default value
    assert (d2.verbosity() == 3);

    // all done
    return 0;
}


// end of file
