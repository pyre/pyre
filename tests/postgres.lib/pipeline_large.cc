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


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that a pipeline sends many statements with large answers before reading any of them,
// without waiting on a server that is waiting on it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // start a pipeline
    auto pipeline = Pipeline(session);

    // the number of statements, whose answers, a kilobyte each, outgrow the buffers of the socket
    // many times over
    const auto statements = 20000;
    // send them all
    for (auto index = 0; index < statements; ++index) {
        // each asking for a kilobyte
        pipeline.execute("SELECT repeat('x', 1024)", arguments_t());
    }
    // mark the end of their segment
    pipeline.sync();

    // read the answers
    auto answers = 0;
    // one at a time
    while (const auto result = pipeline.next()) {
        // each with its row
        if (!result->ok() || result->value(0, 0).size() != 1024) {
            std::cerr << "answer " << answers << " is not the one asked for" << std::endl;
            return 1;
        }
        // count it
        ++answers;
    }
    // all of them
    if (answers != statements) {
        std::cerr << "the pipeline handed back " << answers << " answers" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
