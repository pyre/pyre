// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
template <typename severityT>
using channel_t = pyre::journal::channel_t<severityT>;


// severity stub
class severity_t : public channel_t<severity_t>
{
    // metamethods
public:
    // index initialization is required...
    inline severity_t(const name_type & name): channel_t<severity_t>(name) {}
};


// verify that the default channel state is what we expect
int main() {
    // make a channel
    severity_t channel("test.channel");

    // verify it is on, by default
    assert (channel.active() == true);
    // not fatal
    assert (channel.fatal() == false);
    // and that its device is whatever is set globally
    assert (channel.device() == pyre::journal::chronicler_t::device());

    // all done
    return 0;
}


// end of file
