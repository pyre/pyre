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


// verify that a pipeline sends its statements before any answer is read, and hands back their
// results in the order they were sent, then nothing
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // in a scope of its own
    {
        // start a pipeline
        auto pipeline = Pipeline(session);
        // send three statements
        pipeline.execute("SELECT $1::integer", arguments_t { "1" });
        pipeline.execute("SELECT $1::integer", arguments_t { "2" });
        pipeline.execute("SELECT $1::integer", arguments_t { "3" });
        // and mark the end of their segment
        pipeline.sync();

        // the results arrive in order
        for (const auto expected : { "1", "2", "3" }) {
            // one at a time
            const auto result = pipeline.next();
            // each with its row
            if (!result || !result->ok() || result->value(0, 0) != expected) {
                std::cerr << "the result of the statement for " << expected << " is not next"
                          << std::endl;
                return 1;
            }
        }
        // and then there are no more
        if (pipeline.next()) {
            std::cerr << "the pipeline handed back more results than it sent statements"
                      << std::endl;
            return 1;
        }
    }

    // the session is out of the pipeline, and usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after the pipeline" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
