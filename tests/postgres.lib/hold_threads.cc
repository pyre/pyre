// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test
#include <pyre/postgres.h>
// support
#include <pyre/journal.h>
// so a failing test can say why
#include <iostream>
// the other thread, and how it says it got through
#include <atomic>
#include <chrono>
#include <thread>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that a hold keeps the other threads off its session until it lets go
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // take a hold on it
    auto held = session.hold("a hold");

    // whether the other thread got its statement through
    std::atomic<bool> through = false;
    // start a thread that sends a statement over the same session
    auto other = std::thread([&session, &through]() {
        // send it
        session.exec("SELECT 1");
        // and say so
        through = true;
    });

    // give the other thread time to try
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    // its statement is still waiting
    if (through) {
        std::cerr << "a statement went through while the session was held" << std::endl;
        other.join();
        return 1;
    }

    // let go
    held.release();
    // and the statement of the other thread goes through
    other.join();
    // as it says
    if (!through) {
        std::cerr << "the statement of the other thread did not go through" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
