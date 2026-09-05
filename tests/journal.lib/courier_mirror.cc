// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <unistd.h>


// alias the types
using courier_t = pyre::journal::courier_t;
using chronicler_t = pyre::journal::chronicler_t;
using device_t = pyre::journal::device_t;


// a device that counts what it is handed, by sink
class Counter : public device_t {
    // metamethods
public:
    ~Counter() {}
    Counter() : device_t("counter"), alerts(0), helps(0), memos(0) {}

    // interface
public:
    virtual auto alert(const entry_type &) -> Counter &
    {
        ++alerts;
        return *this;
    }
    virtual auto help(const entry_type &) -> Counter &
    {
        ++helps;
        return *this;
    }
    virtual auto memo(const entry_type &) -> Counter &
    {
        ++memos;
        return *this;
    }

    // data
public:
    int alerts;
    int helps;
    int memos;
};


// a mirror sees every entry through its own sink, whether or not the far end is there
int
main()
{
    // make a pipe
    int pipes[2];
    assert(::pipe(pipes) == 0);
    // a mirror
    auto mirror = std::make_shared<Counter>();
    // a courier that also delivers to it
    auto courier = std::make_shared<courier_t>(pipes[1], "courier", mirror);
    assert(courier->mirror() == mirror);
    chronicler_t::device(courier);

    // log through three sinks
    pyre::journal::info_t one("test.courier.mirror");
    one << "one" << pyre::journal::endl;
    pyre::journal::debug_t debug("test.courier.mirror");
    debug.activate();
    debug << "two" << pyre::journal::endl;
    pyre::journal::help_t three("test.courier.mirror");
    three << "three" << pyre::journal::endl;

    // the mirror saw all three, through the right sinks
    assert(mirror->alerts == 1);
    assert(mirror->memos == 1);
    assert(mirror->helps == 1);
    // and so did the far end
    assert(courier->shipped() == 3);
    // drain it
    char buffer[64 * 1024];
    auto got = ::read(pipes[0], buffer, sizeof(buffer));
    assert(got > 0);
    assert(std::count(buffer, buffer + got, '\n') == 3);

    // take the far end away
    ::close(pipes[0]);
    // log again; this must not take the process down
    pyre::journal::info_t four("test.courier.mirror");
    four << "four" << pyre::journal::endl;
    // the courier went quiet
    assert(courier->dead());
    assert(courier->shipped() == 3);
    // but the mirror still hears everything
    assert(mirror->alerts == 2);

    // clean up
    courier->close();

    // all done
    return 0;
}


// end of file
