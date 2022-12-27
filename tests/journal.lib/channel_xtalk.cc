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


// severity stubs
// info
class myinfo_t :
    public channel_t<myinfo_t>
{
    // types
public:
    using channel_type = channel_t<myinfo_t>;

    // metamethods
public:
    // index initialization is required...
    explicit myinfo_t(const name_type &);

    // implementation details
public:
    // initialize the channel index
    static inline auto initializeIndex() -> index_type;
};

// info stub implementation
myinfo_t::myinfo_t(const name_type & name) :
    channel_type(name)
{}

// initialize the channel index
auto myinfo_t::initializeIndex() -> index_type
{
    // make an empty index; for {myinfo_t}, channels are (inactive,non-fatal) by default
    return index_type(false, false);
}


// warning
class mywarning_t :
    public channel_t<mywarning_t>
{
    // types
public:
    using channel_type = channel_t<mywarning_t>;

    // metamethods
public:
    // index initialization is required...
    explicit mywarning_t(const name_type &);

    // implementation details
public:
    // initialize the channel index
    static inline auto initializeIndex() -> index_type;
};

// warning stub implementation
mywarning_t::mywarning_t(const name_type & name) :
    channel_type(name)
{}

// initialize the channel index
auto mywarning_t::initializeIndex() -> index_type
{
    // make an empty index; for {mywarning_t}, channels are (active,non-fatal) by default
    return index_type(true, false);
}


// error
class myerror_t :
    public channel_t<myerror_t>
{
    // types
public:
    using channel_type = channel_t<myerror_t>;

    // metamethods
public:
    // index initialization is required...
    explicit myerror_t(const name_type &);

    // implementation details
public:
    // initialize the channel index
    static inline auto initializeIndex() -> index_type;
};

// error stub implementation
myerror_t::myerror_t(const name_type & name) :
    channel_type(name)
{}

// initialize the channel index
auto myerror_t::initializeIndex() -> index_type
{
    // make an empty index; for {myerror_t}, channels are (active,fatal) by default
    return index_type(true, true);
}


// verify there is no crosstalk among the indices of different severities, and that the indices
// update correctly when new channels are made
int main() {
    // make a couple of info channels
    myinfo_t info_1("channel_1");
    myinfo_t info_2("channel_2");
    // a couple of warning channels
    mywarning_t warning_1("channel_1");
    mywarning_t warning_2("channel_2");
    // and a couple of error channels
    myerror_t error_1("channel_1");
    myerror_t error_2("channel_2");

    // get the indices
    const myinfo_t::index_type & infos = info_1.index();
    const mywarning_t::index_type & warnings = warning_1.index();
    const myerror_t::index_type & errors = error_1.index();

    // verify we have set up the channels correctly
    assert (infos.active() == false);
    assert (infos.fatal() == false);
    assert (warnings.active() == true);
    assert (warnings.fatal() == false);
    assert (errors.active() == true);
    assert (errors.fatal() == true);

    // check the states
    assert (info_1.active() == infos.active());
    assert (info_2.active() == infos.active());
    assert (warning_1.active() == warnings.active());
    assert (warning_2.active() == warnings.active());
    assert (error_1.active() == errors.active());
    assert (error_2.active() == errors.active());

    assert (info_1.fatal() == infos.fatal());
    assert (info_2.fatal() == infos.fatal());
    assert (warning_1.fatal() == warnings.fatal());
    assert (warning_2.fatal() == warnings.fatal());
    assert (error_1.fatal() == errors.fatal());
    assert (error_2.fatal() == errors.fatal());

    // verify it has exactly two channels
    assert (infos.size() == 2);
    // one of them is "channel1"
    assert (infos.contains("channel_1"));
    // and the other is "channel2"
    assert (infos.contains("channel_2"));

    // verify it has exactly two channels
    assert (warnings.size() == 2);
    // one of them is "channel1"
    assert (warnings.contains("channel_1"));
    // and the other is "channel2"
    assert (warnings.contains("channel_2"));

    // verify it has exactly two channels
    assert (errors.size() == 2);
    // one of them is "channel1"
    assert (errors.contains("channel_1"));
    // and the other is "channel2"
    assert (errors.contains("channel_2"));

    // all done
    return 0;
}


// end of file
