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


// verify that the result of a statement in a pipeline can be read before its segment is synced
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // start a pipeline
    auto pipeline = Pipeline(session);
    // send a statement, without a sync
    pipeline.execute("SELECT 42", arguments_t());
    // its result arrives anyway
    const auto result = pipeline.next();
    // with its row
    if (!result || !result->ok() || result->value(0, 0) != "42") {
        std::cerr << "the result of a statement before its sync did not arrive" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
