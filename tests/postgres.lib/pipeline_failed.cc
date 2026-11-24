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


// verify that a statement that fails in a pipeline fails its segment: its result says why, the
// statements after it in the segment are skipped, the ones before it are undone, and the next
// segment runs
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_pipeline (id integer PRIMARY KEY)");
    // with a row
    session.exec("INSERT INTO pyre_pipeline (id) VALUES (1)");

    // the statement that adds a row
    const auto insert = "INSERT INTO pyre_pipeline (id) VALUES ($1::integer)";
    // in a scope of its own
    {
        // start a pipeline
        auto pipeline = Pipeline(session);
        // a segment whose second statement fails
        pipeline.execute(insert, arguments_t { "2" });
        pipeline.execute(insert, arguments_t { "1" });
        pipeline.execute(insert, arguments_t { "3" });
        pipeline.sync();
        // and a segment that runs
        pipeline.execute(insert, arguments_t { "4" });
        pipeline.sync();

        // the first statement ran
        const auto first = pipeline.next();
        if (!first || !first->ok()) {
            std::cerr << "the first statement did not run" << std::endl;
            return 1;
        }
        // the second failed, as the server says
        const auto second = pipeline.next();
        if (!second || second->ok() || second->status() != ExecStatus::fatalError) {
            std::cerr << "the duplicate did not fail" << std::endl;
            return 1;
        }
        // the third was skipped
        const auto third = pipeline.next();
        if (!third || third->status() != ExecStatus::pipelineAborted) {
            std::cerr << "the statement after the failure was not skipped" << std::endl;
            return 1;
        }
        // and the one of the next segment ran
        const auto fourth = pipeline.next();
        if (!fourth || !fourth->ok()) {
            std::cerr << "the statement of the next segment did not run" << std::endl;
            return 1;
        }
    }

    // the table holds the row it had, and the one of the second segment
    const auto rows = session.exec("SELECT id FROM pyre_pipeline ORDER BY id");
    if (rows.rows() != 2 || rows.value(0, 0) != "1" || rows.value(1, 0) != "4") {
        std::cerr << "the failed segment was not undone" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
