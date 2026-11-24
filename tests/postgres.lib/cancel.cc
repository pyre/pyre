// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test
#include <pyre/postgres.h>
// so a failing test can say why
#include <iostream>
// the thread that asks for the cancellation
#include <chrono>
#include <thread>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that a statement in flight stops when another thread asks the server to give up on it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;
    // and the clock
    using steady_t = std::chrono::steady_clock;

    // open a session
    const auto session = Connection(specification());

    // the other thread waits until the statement is surely under way, and asks for it to stop
    auto canceller = std::thread([&session]() -> void {
        // give the statement time to reach the server
        std::this_thread::sleep_for(std::chrono::milliseconds(300));
        // and ask
        session.cancel();
        // all done
        return;
    });

    // note the time
    const auto start = steady_t::now();
    // attempt to
    try {
        // run a statement that would take ten seconds
        session.exec("SELECT pg_sleep(10)");
        // which must not finish
        std::cerr << "the statement ran to the end" << std::endl;
        canceller.join();
        return 1;
    }
    // the way the server reports a statement it gave up on
    catch (const OperationalError & error) {
        // with its own code for it
        if (error.diagnostic().sqlstate() != "57014") {
            std::cerr << "the statement failed with " << error.diagnostic().sqlstate() << std::endl;
            canceller.join();
            return 1;
        }
    }
    // the time the statement took
    const auto elapsed = steady_t::now() - start;
    // wait for the other thread
    canceller.join();

    // the statement stopped well before it would have finished
    if (elapsed > std::chrono::seconds(5)) {
        std::cerr << "the statement took "
                  << std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count()
                  << " ms to stop" << std::endl;
        return 1;
    }
    // and the session is usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after the cancellation" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
