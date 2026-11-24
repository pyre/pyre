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
// the values of the runs
#include <string>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that a pipeline prepares a statement and runs it many times, and that every run lands
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_pipeline (id integer)");

    // the number of runs
    const auto runs = 100;
    // in a scope of its own
    {
        // start a pipeline
        auto pipeline = Pipeline(session);
        // teach the server the insert
        pipeline.prepare("pyre_pipeline_insert", "INSERT INTO pyre_pipeline (id) VALUES ($1)");
        // run it many times
        for (auto run = 0; run < runs; ++run) {
            // each with its own value
            pipeline.execPrepared("pyre_pipeline_insert", arguments_t { std::to_string(run) });
        }
        // mark the end of the segment
        pipeline.sync();
        // go through the results: the preparation's, and one for each run
        for (auto index = 0; index <= runs; ++index) {
            // each one
            const auto result = pipeline.next();
            // says its statement ran
            if (!result || !result->ok()) {
                std::cerr << "statement " << index << " of the pipeline did not run" << std::endl;
                return 1;
            }
        }
    }

    // every run landed
    if (session.exec("SELECT count(*) FROM pyre_pipeline").value(0, 0) != std::to_string(runs)) {
        std::cerr << "the table does not hold a row for each run" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
