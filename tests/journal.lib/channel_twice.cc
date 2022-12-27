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


// verify that channels of the same severity and name share the same state
int main() {
    // make a channel
    severity_t channel_1("test.channel");
    // verify it's on
    assert (channel_1);
    // deactivate it
    channel_1.deactivate();
    // and check
    assert (!channel_1);

    // access again through another variable
    severity_t channel_2("test.channel");
    // verify it's off
    assert (!channel_2);
    // activate it
    channel_2.activate();
    // check
    assert (channel_2);
    // verify that {channel_1} mirrors the new settings
    assert (channel_1);

    // all done
    return 0;
}


// end of file
