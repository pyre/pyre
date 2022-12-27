// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// channel stub
class channel_t : public pyre::journal::channel_t<channel_t> {
    // metamethods
public:
    inline explicit channel_t(const name_type & name) :
        pyre::journal::channel_t<channel_t>(name) {}

    // implementation details
    inline void record() {}
    inline void die() {}
};


// compile time: make sure injection works as expected
int main() {
    // make a channel
    channel_t channel("channel");

    // inject something
    channel
        << pyre::journal::note("time", "now")
        << "hello world!" << pyre::journal::newline
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
