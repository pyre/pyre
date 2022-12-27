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


// exercise the channel state interface for both the shared and global state
int main() {
    // make a channel
    severity_t channel("test.channel");

    // verify its name
    assert (channel.name() == "test.channel");
    // its activation state
    assert (channel.active() == true);
    // whether it's fatal
    assert (channel.fatal() == false);
    // and again using the conversion to bool
    assert (channel);
    // verify that the default activation state is as expected
    assert (channel.index().active() == true);
    // verify that the default fatal state is as expected
    assert (channel.index().fatal() == false);

    // deactivate it
    channel.deactivate();
    // and check
    assert (channel.active() == false);

    // make it fatal
    channel.fatal(true);
    // and check
    assert (channel.fatal() == true);

    // all done
    return 0;
}


// end of file
