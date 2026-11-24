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
// threads
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


// verify that a copy keeps the other threads off its session until it ends, so that a statement
// sent by one of them waits for the copy, rather than abandoning it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)");

    // start a copy into it
    auto copy = CopyIn(session, "COPY pyre_copy FROM STDIN");
    // send a row
    copy.record(1);

    // whether the other thread got its statement through
    std::atomic<bool> through = false;
    // start a thread that sends a statement over the same session
    auto other = std::thread([&session, &through]() {
        // send it
        session.exec("INSERT INTO pyre_copy VALUES (2)");
        // and say so
        through = true;
    });

    // give the other thread time to try
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    // its statement is still waiting
    if (through) {
        std::cerr << "a statement went through while the copy was under way" << std::endl;
        other.join();
        return 1;
    }

    // send another row
    copy.record(3);
    // and finish, which the statement of the other thread would have spoiled
    copy.end();
    // the statement of the other thread goes through now
    other.join();

    // all three rows are in
    const auto rows = session.exec("SELECT count(*) FROM pyre_copy");
    // so say
    if (rows.value(0, 0) != "3") {
        std::cerr << "the table holds " << rows.value(0, 0) << " rows" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
