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
// the workers
#include <atomic>
#include <thread>
#include <vector>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that several threads can run statements through one session, each getting its own
// answers back
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // the number of answers that were not what their thread asked for
    std::atomic<int> problems = 0;

    // each worker asks for its own number back, many times over
    auto worker = [&session, &problems](int number) -> void {
        // many times
        for (auto round = 0; round < 50; ++round) {
            // ask for my number back
            const auto answer = session.execute("SELECT $1::int", number)[0][0].as<int>();
            // and if it is not mine
            if (answer != number) {
                // make a note
                ++problems;
            }
        }
        // all done
        return;
    };

    // the threads
    std::vector<std::thread> threads;
    // start a few
    for (auto number = 0; number < 4; ++number) {
        // each with its own number
        threads.emplace_back(worker, number);
    }
    // and wait for all of them
    for (auto & thread : threads) {
        // one at a time
        thread.join();
    }

    // every answer must have been the one its thread asked for
    if (problems != 0) {
        // so complain
        std::cerr << problems << " answers went to the wrong thread" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
