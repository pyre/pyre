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


// verify that a pipeline that goes away before its results are read syncs what it sent, reads the
// answers to the end, and leaves the session out of the pipeline and usable
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_pipeline (id integer)");

    // in a scope of its own
    {
        // start a pipeline
        auto pipeline = Pipeline(session);
        // send two inserts, without a sync
        pipeline.execute("INSERT INTO pyre_pipeline (id) VALUES (1)", arguments_t());
        pipeline.execute("INSERT INTO pyre_pipeline (id) VALUES (2)", arguments_t());
        // and leave without reading anything
    }

    // the session is free
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session is not free after an abandoned pipeline" << std::endl;
        return 1;
    }
    // and the inserts were synced, so they kept their work
    if (session.exec("SELECT count(*) FROM pyre_pipeline").value(0, 0) != "2") {
        std::cerr << "the statements of an abandoned pipeline were lost" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
