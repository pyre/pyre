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


// the trash can
using trash_t = pyre::journal::trash_t;


// verify that we can control the default device
int main() {
    // get the default device
    auto builtin = severity_t::index().device();

    // make a new device
    auto custom = std::make_shared<trash_t>();
    // install it
    severity_t::index().device(custom);

    // check that the current device is the one we just installed
    assert (severity_t::index().device() == custom);

    // all done
    return 0;
}


// end of file
