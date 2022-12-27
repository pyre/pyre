// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// channel stub
class severity_t : public pyre::journal::channel_t<severity_t> {
    // metamethods
public:
    inline explicit severity_t(const name_type & name, detail_type detail = 1) :
        pyre::journal::channel_t<severity_t>(name, detail) {}
};


// verify that diagnostics can be instantiated correctly
int main() {
    // make a diagnostic
    severity_t d1("d1");
    // make sure its detail is at the default value
    assert (d1.detail() == 1);

    // make another diagnostic with a non-default detail
    severity_t d2("d3", 3);
    // make sure its detail is at the default value
    assert (d2.detail() == 3);

    // all done
    return 0;
}


// end of file
