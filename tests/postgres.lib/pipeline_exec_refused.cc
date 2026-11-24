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


// verify that a statement sent through the session of a pipeline, rather than through the
// pipeline, is refused as a misuse of the interface, whether or not the pipeline has answers
// still to read
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // start a pipeline
    auto pipeline = Pipeline(session);

    // a pipeline with nothing in flight, and one with a statement whose answer is unread
    for (const auto inFlight : { false, true }) {
        // the second time around
        if (inFlight) {
            // send a statement through the pipeline
            pipeline.execute("SELECT 1", arguments_t());
        }
        // attempt to
        try {
            // send another through the session
            session.exec("SELECT 42");
            // which must fail
            std::cerr << "a statement sent around a pipeline was accepted" << std::endl;
            return 1;
        }
        // as a misuse of the interface
        catch (const InterfaceError & error) {
            // that names the statement
            if (error.diagnostic().command() != "SELECT 42") {
                std::cerr << "the refusal named " << error.diagnostic().command() << std::endl;
                return 1;
            }
        }
    }

    // the statement in the pipeline still hands back its result
    const auto result = pipeline.next();
    // with its row
    if (!result || !result->ok() || result->value(0, 0) != "1") {
        std::cerr << "the pipeline lost its statement" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
